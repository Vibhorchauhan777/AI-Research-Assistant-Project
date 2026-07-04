from app.search import search_web
from app.llm import get_llm
from app.prompts import RESEARCH_SYSTEM_PROMPT

llm = get_llm()


def search_node(state):
    """
    Adds search results into state
    """
    results = search_web(state["query"], max_results=5)
    state["context"] = results
    return state


def fast_node(state):
    """
    Fast answer generation (short response)
    """

    context_text = "\n\n".join(
    f"TITLE: {r['title']}\nCONTENT: {r['content'][:400]}\nSOURCE: {r.get('source','')}"
    for r in state["context"]
)

    response = llm.invoke([
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", f"""
Question: {state['query']}

Context:
{context_text}

Give a short and precise answer.
""")
    ])

    state["final"] = response.content
    return state


def deep_node(state):
    """
    Deep research answer generation
    """

    context_text = "\n\n".join(
    f"TITLE: {r['title']}\nCONTENT: {r['content'][:400]}\nSOURCE: {r.get('source','')}"
    for r in state["context"]
)

    response = llm.invoke([
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", f"""
Question: {state['query']}

Context:
{context_text}

Give a detailed, structured explanation.
""")
    ])

    state["final"] = response.content
    return state