# Name: Kofi Appiah
# Index: 10022300106
# File: rag/embedder.py
# Purpose: Generate embeddings and store in FAISS vector index

import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "embeddings/faiss.index"
CHUNKS_PATH = "embeddings/chunks.pkl"

# Load the embedding model once
model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks):
    """Generate embeddings for all chunks."""
    print(f"Embedding {len(chunks)} chunks with {MODEL_NAME}...")
    texts = [c["text"] for c in chunks]

    embeddings = []
    batch_size = 32

    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, convert_to_numpy=True)
        embeddings.append(batch_embeddings)

    embeddings = np.vstack(embeddings).astype(np.float32)
    print(f"Embeddings shape: {embeddings.shape}")
    return embeddings


def build_index(chunks):
    """Build FAISS index and save to disk."""
    embeddings = embed_chunks(chunks)

    # Build FAISS flat L2 index
    dim = embeddings.shape[1]  # 384 for MiniLM
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and chunks
    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"FAISS index saved → {INDEX_PATH} ({index.ntotal} vectors)")
    print(f"Chunks saved → {CHUNKS_PATH}")
    return index, chunks


def load_index():
    """Load FAISS index and chunks from disk."""
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"Loaded index with {index.ntotal} vectors")
    return index, chunks


def embed_query(query):
    """Embed a single query string."""
    return model.encode([query], convert_to_numpy=True).astype(np.float32)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rag.chunker import chunk_all

    with open("data/clean_elections.txt", "r", encoding="utf-8") as f:
        csv_text = f.read()
    with open("data/clean_budget.txt", "r", encoding="utf-8") as f:
        pdf_text = f.read()

    chunks = chunk_all(csv_text, pdf_text)
    build_index(chunks)