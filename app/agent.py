from app.search import search_web
from app.llm import get_llm
from app.prompts import RESEARCH_SYSTEM_PROMPT
from app.state import AgentState
from app.router import classify_query
from app.logger import Logger

llm = get_llm()
logger = Logger()


def run_agent(state: AgentState) -> AgentState:

    # -------------------------
    # STEP 0: ROUTING
    # -------------------------
    mode = classify_query(state.query)
    print(f"\n[ROUTER] Mode selected: {mode.upper()}")

    # -------------------------
    # FAST MODE
    # -------------------------
    if mode == "fast":

        logger.start()

        results = search_web(state.query, max_results=3)

        context_text = "\n".join(
            f"{r['title']}: {r['content'][:200]}"
            for r in results
        )

        response = llm.invoke([
            ("system", RESEARCH_SYSTEM_PROMPT),
            ("user", f"""
        Question: {state.query}

        Context:
        {context_text}

        Give a short, accurate, and direct answer.
        """)
        ])

        logger.end("FAST MODE (Search + LLM)")

        state.final = response.content
        state.context = results
        state.iteration = 1

        return state

    # -------------------------
    # DEEP MODE
    # -------------------------
    logger.start()

    results = search_web(state.query, max_results=5)

    context_text = "\n".join(
        f"{r['title']}: {r['content']}"
        for r in results
    )

    response = llm.invoke([
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", f"""
    Question: {state.query}

    Context:
    {context_text}

    Write a detailed, structured, research-grade explanation.
    Include reasoning, comparisons if relevant, and clarity.
    """)
    ])

    logger.end("DEEP MODE (Search + LLM)")

    state.final = response.content
    state.context = results
    state.iteration = 1

    return state