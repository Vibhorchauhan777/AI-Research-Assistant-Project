import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

DIM = 384

index = faiss.IndexFlatL2(DIM)

memory_store = []


def add_memory(text: str):
    embedding = model.encode([text])[0]
    embedding = np.array([embedding]).astype("float32")

    index.add(embedding)
    memory_store.append(text)


def search_memory(query: str, k: int = 5):
    if len(memory_store) == 0:
        return []

    query_vec = model.encode([query])[0]
    query_vec = np.array([query_vec]).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        if i < len(memory_store):
            results.append(memory_store[i])

    return results