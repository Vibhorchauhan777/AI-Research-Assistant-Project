from app.search import search_web

results = search_web("What is LangGraph?")

for r in results:
    print("\n---")
    print(r["title"])
    print(r["url"])
    print(r["content"][:200])