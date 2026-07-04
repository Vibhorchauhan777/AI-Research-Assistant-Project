from typing import TypedDict, List, Dict, Any
import re
import json

from langgraph.graph import StateGraph, END

from app.llm import get_llm
from app.router import classify_query
from app.prompts import RESEARCH_SYSTEM_PROMPT
from app.memory import init_db, save_memory
from app.vector_memory import add_memory, search_memory
from app.search import search_web
from app.tools import wikipedia_search, arxiv_search


# =========================
# INIT
# =========================
llm = get_llm()
init_db()


# =========================
# STATE
# =========================
class AgentState(TypedDict):
    query: str
    mode: str
    plan: Dict[str, Any]
    output: Dict[str, Any]
    trace: List[str]

    memory: List[Dict[str, Any]]
    context: List[Dict[str, Any]]

    draft: str
    final: str

    score: int
    iterations: int


# =========================
# ROUTER
# =========================
def route_node(state: AgentState):
    state["trace"].append("🧭 Routing query")
    state["mode"] = classify_query(state["query"])
    state["iterations"] = 0
    return state


# =========================
# MEMORY
# =========================
def memory_node(state: AgentState):
    state["trace"].append("🧠 Searching memory")
    state["memory"] = search_memory(state["query"], k=5)
    return state


# =========================
# PLANNER (FIXED)
# =========================
def planner_node(state: AgentState):
    state["trace"].append("📝 Planning research")

    prompt = f"""
Return ONLY valid JSON:

{{
  "use_web": true,
  "use_wiki": true,
  "use_arxiv": true,
  "mode": "fast"
}}

Query: {state['query']}
"""

    response = llm.invoke([("user", prompt)])

    try:
        plan = json.loads(response.content)
    except:
        plan = {
            "use_web": True,
            "use_wiki": True,
            "use_arxiv": True,
            "mode": "deep"
        }

    state["plan"] = plan
    state["mode"] = plan.get("mode", "deep")

    return state


# =========================
# TOOL EXECUTION (STEP 21 TRACE DONE)
# =========================
def tool_node(state: AgentState):
    state["trace"].append("🌐 Searching sources")

    plan = state.get("plan", {})
    query = state["query"]

    results = []

    if plan.get("use_web"):
        state["trace"].append("🔎 Tavily/Web search")
        results += search_web(query, max_results=3)

    if plan.get("use_wiki"):
        state["trace"].append("📚 Wikipedia search")
        results += wikipedia_search(query, k=2)

    if plan.get("use_arxiv"):
        state["trace"].append("📄 Arxiv search")
        results += arxiv_search(query, k=2)

    state["context"] = results
    state["trace"].append(f"✅ Collected {len(results)} sources")

    return state


# =========================
# FAST MODE
# =========================
def fast_node(state: AgentState):
    state["trace"].append("⚡ Fast answer generation")

    memory_text = "\n".join(str(m) for m in state.get("memory", []))

    context_text = "\n".join(
        f"{r.get('title','No Title')}: {r.get('content','')[:200]}"
        for r in state.get("context", [])
    )

    response = llm.invoke([
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", f"""
FAST MODE

Q: {state['query']}

Memory:
{memory_text}

Context:
{context_text}
""")
    ])

    state["final"] = response.content
    return state


# =========================
# DEEP MODE
# =========================
def deep_node(state: AgentState):
    state["trace"].append("🤖 Deep reasoning")

    memory_text = "\n".join(str(m) for m in state.get("memory", []))

    context_text = "\n".join(
        f"{r.get('title','No Title')}: {r.get('content','')}"
        for r in state.get("context", [])
    )

    response = llm.invoke([
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", f"""
DEEP MODE

Q: {state['query']}

Memory:
{memory_text}

Context:
{context_text}

Provide structured explanation.
""")
    ])

    state["draft"] = response.content
    return state


# =========================
# REFLECTION
# =========================
def reflect_node(state: AgentState):
    state["trace"].append("🔍 Evaluating answer")

    response = llm.invoke([
        ("user", f"""
Score 0-10 only.

Q: {state['query']}
A: {state.get('draft','')}
""")
    ])

    match = re.search(r"\d+", response.content)
    score = int(match.group()) if match else 5

    state["score"] = score
    state["trace"].append(f"⭐ Score: {score}/10")

    return state


# =========================
# REFINEMENT
# =========================
def refine_node(state: AgentState):
    state["trace"].append("✏️ Refining answer")

    response = llm.invoke([
        ("user", f"""
Improve this answer:

{state.get('draft','')}
""")
    ])

    state["draft"] = response.content
    state["iterations"] += 1

    return state


# =========================
# FINAL NODE
# =========================
def final_node(state: AgentState):
    state["trace"].append("🏁 Finalizing response")

    result = state.get("draft") or state.get("final")

    state["final"] = result

    add_memory(f"Q: {state['query']}\nA: {result}")
    save_memory(state["query"], result)

    state["output"] = {
        "answer": result,
        "sources": state.get("context", []),
        "mode": state.get("mode", "unknown"),
        "trace": state.get("trace", [])
    }

    return state


# =========================
# DECISION LOGIC
# =========================
def decide_mode(state: AgentState):
    return state["mode"]


def should_retry(state: AgentState):
    if state.get("score", 0) < 7 and state.get("iterations", 0) < 2:
        return "retry"
    return "end"


# =========================
# GRAPH
# =========================
graph = StateGraph(AgentState)

graph.add_node("route", route_node)
graph.add_node("planner", planner_node)
graph.add_node("memory_fetch", memory_node)
graph.add_node("tools", tool_node)

graph.add_node("fast", fast_node)
graph.add_node("deep", deep_node)

graph.add_node("reflect", reflect_node)
graph.add_node("refine", refine_node)

graph.add_node("final_writer", final_node)

graph.set_entry_point("route")

graph.add_edge("route", "planner")
graph.add_edge("planner", "memory_fetch")
graph.add_edge("memory_fetch", "tools")

graph.add_conditional_edges(
    "tools",
    decide_mode,
    {
        "fast": "fast",
        "deep": "deep"
    }
)

graph.add_edge("fast", "final_writer")
graph.add_edge("deep", "reflect")

graph.add_conditional_edges(
    "reflect",
    should_retry,
    {
        "retry": "refine",
        "end": "final_writer"
    }
)

graph.add_edge("refine", "reflect")
graph.add_edge("final_writer", END)

app = graph.compile()


# =========================
# ENTRY
# =========================
def run_graph(query: str):
    result = app.invoke({
        "query": query,
        "mode": "",
        "plan": {},
        "memory": [],
        "context": [],
        "draft": "",
        "final": "",
        "score": 0,
        "iterations": 0,
        "output": {},
        "trace": []
    })

    output = result.get("output", {})

    return {
        "answer": output.get("answer", result.get("final", "")),
        "sources": output.get("sources", result.get("context", [])),
        "mode": output.get("mode", result.get("mode", "")),
        "trace": output.get("trace", result.get("trace", []))
    }