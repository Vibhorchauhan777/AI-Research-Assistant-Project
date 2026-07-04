from app.router import classify_query
from app.nodes import search_node, fast_node, deep_node


def run_graph(query: str):

    state = {
        "query": query,
        "context": [],
        "final": "",
        "mode": ""
    }

    state["mode"] = classify_query(query)

    state = search_node(state)

    if state["mode"] == "fast":
        state = fast_node(state)
    else:
        state = deep_node(state)

    return state