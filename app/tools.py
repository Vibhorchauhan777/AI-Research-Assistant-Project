import wikipedia
import arxiv


# -------------------------
# WIKIPEDIA TOOL
# -------------------------
def wikipedia_search(query: str, k: int = 3):
    try:
        results = wikipedia.search(query, results=k)

        pages = []
        for title in results:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                pages.append({
                    "title": page.title,
                    "content": page.summary[:800],
                    "source": page.url
                })
            except:
                continue

        return pages

    except Exception:
        return []


# -------------------------
# ARXIV TOOL
# -------------------------


def arxiv_search(query: str, k: int = 5):
    search = arxiv.Search(
        query=query,
        max_results=k,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []

    try:
        client = arxiv.Client()
        papers = client.results(search)
    except TypeError:
        papers = search.results()

    for paper in papers:
        results.append({
            "title": paper.title,
            "content": paper.summary,
            "url": paper.entry_id
        })

    return results