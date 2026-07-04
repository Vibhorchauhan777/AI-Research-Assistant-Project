from app.llm import get_llm

llm = get_llm()


def classify_query(query: str) -> str:
    """
    Returns FAST or DEEP based on query complexity.
    """

    prompt = f"""
You are a routing system for an AI research agent.

Classify the query into one of two categories:

FAST:
- simple factual questions
- short explanations
- news updates
- direct answers

DEEP:
- comparisons
- technical topics
- research questions
- multi-step reasoning

Return ONLY one word: FAST or DEEP

Query: {query}
"""

    response = llm.invoke([
        ("user", prompt)
    ])

    result = response.content.strip().upper()

    if "DEEP" in result:
        return "deep"

    return "fast"