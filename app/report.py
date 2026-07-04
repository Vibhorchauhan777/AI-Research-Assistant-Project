from datetime import datetime


def format_search_results(results: list):
    """
    Converts search results into a single context string for LLM.
    """

    context = ""

    for i, r in enumerate(results, 1):
        context += f"""
Result {i}:
Title: {r['title']}
URL: {r['url']}
Content: {r['content']}
---
"""

    return context


def build_markdown_report(title: str, summary: str, key_points: list, explanation: str, sources: list):
    """
    Builds final markdown report.
    """

    markdown = f"""
# {title}

## Summary
{summary}

## Key Points
"""

    for point in key_points:
        markdown += f"- {point}\n"

    markdown += f"""

## Detailed Explanation
{explanation}

## Sources
"""

    for src in sources:
        markdown += f"- {src}\n"

    markdown += f"""

---
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return markdown