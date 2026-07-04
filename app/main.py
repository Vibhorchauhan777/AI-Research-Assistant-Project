from app.search import search_web
from app.llm import get_llm
from app.prompts import RESEARCH_SYSTEM_PROMPT, RESEARCH_USER_PROMPT
from app.report import format_search_results

import re


def extract_sections(text: str):
    """
    Basic parser to extract structured sections from LLM output.
    """

    def grab(pattern):
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    title = grab(r"# Title\s*(.*?)\n# Summary")
    summary = grab(r"# Summary\s*(.*?)\n# Key Points")
    key_points_block = grab(r"# Key Points\s*(.*?)\n# Detailed Explanation")
    explanation = grab(r"# Detailed Explanation\s*(.*?)\n# Sources")
    sources_block = grab(r"# Sources\s*(.*)")

    key_points = [
        line.strip("- ").strip()
        for line in key_points_block.split("\n")
        if line.strip().startswith("-")
    ]

    sources = [
        line.strip("- ").strip()
        for line in sources_block.split("\n")
        if line.strip().startswith("-")
    ]

    return title, summary, key_points, explanation, sources


def run_research(query: str):
    """
    End-to-end AI research pipeline.
    """

    print("\nSearching web...")
    results = search_web(query)

    print("Formatting context...")
    context = format_search_results(results)

    print("Loading LLM...")
    llm = get_llm()

    print("Generating response...")

    prompt = RESEARCH_USER_PROMPT.format(
        question=query,
        context=context
    )

    messages = [
        ("system", RESEARCH_SYSTEM_PROMPT),
        ("user", prompt),
    ]

    response = llm.invoke(messages)

    print("Response received")

    title, summary, key_points, explanation, sources = extract_sections(response.content)

    return {
        "title": title,
        "summary": summary,
        "key_points": key_points,
        "explanation": explanation,
        "sources": sources,
        "raw": response.content
    }


if __name__ == "__main__":

    query = input("\nEnter your research question: ")

    result = run_research(query)

    print("\n\n-------------------------FINAL REPORT------------------------ \n")
    print("TITLE:", result["title"])
    print("\nSUMMARY:\n", result["summary"])

    print("\nKEY POINTS:")
    for kp in result["key_points"]:
        print("-", kp)

    print("\nEXPLANATION:\n", result["explanation"])

    print("\nSOURCES:")
    for s in result["sources"]:
        print("-", s)