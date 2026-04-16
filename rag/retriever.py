# Name: Kofi Appiah
# Index: 10022300106
# File: rag/retriever.py
# Purpose: Retrieve relevant chunks using vector search + hybrid search

import numpy as np
from rank_bm25 import BM25Okapi
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.embedder import embed_query, load_index


def vector_search(query, index, chunks, top_k=5):
    """Pure vector similarity search using FAISS."""
    query_vec = embed_query(query)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(chunks):
            results.append({
                "chunk": chunks[idx],
                "score": float(1 / (1 + dist)),  # convert distance to similarity
                "method": "vector"
            })
    return results


def keyword_search(query, chunks, top_k=5):
    """BM25 keyword search."""
    tokenized_corpus = [c["text"].lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "chunk": chunks[idx],
            "score": float(scores[idx]),
            "method": "keyword"
        })
    return results


def hybrid_search(query, index, chunks, top_k=5):
    """
    Hybrid search: combine vector + keyword results.
    This is the innovation for Part B — merges both signals
    so we catch both semantic and exact keyword matches.
    """
    vector_results = vector_search(query, index, chunks, top_k=top_k)
    keyword_results = keyword_search(query, chunks, top_k=top_k)

    # Merge and deduplicate by chunk_id, keeping highest score
    seen = {}
    for r in vector_results + keyword_results:
        cid = r["chunk"]["chunk_id"]
        if cid not in seen or r["score"] > seen[cid]["score"]:
            seen[cid] = r

    # Sort by score descending
    merged = sorted(seen.values(), key=lambda x: x["score"], reverse=True)
    return merged[:top_k]


def retrieve(query, index, chunks, top_k=5, method="hybrid"):
    """Main retrieval function."""
    if method == "vector":
        return vector_search(query, index, chunks, top_k)
    elif method == "keyword":
        return keyword_search(query, chunks, top_k)
    else:
        return hybrid_search(query, index, chunks, top_k)


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from rag.embedder import load_index

    index, chunks = load_index()

    # Test queries
    queries = [
        "Who won the 2020 election in Ashanti region?",
        "What is the budget allocation for education in 2025?",
        "NDC votes in Accra",
    ]

    for q in queries:
        print(f"\nQuery: {q}")
        print("-" * 50)
        results = retrieve(q, index, chunks, top_k=3)
        for i, r in enumerate(results):
            print(f"[{i+1}] Score: {r['score']:.4f} | Source: {r['chunk']['source']} | Method: {r['method']}")
            print(f"     {r['chunk']['text'][:150]}...")