# Name: Kofi Appiah
# Index: 10022300106
# File: rag/chunker.py
# Purpose: Chunk cleaned text into overlapping segments for retrieval

def chunk_text(text, chunk_size=500, overlap=50, source="unknown"):
    """
    Split text into overlapping chunks.

    Design decisions:
    - chunk_size=500 words: large enough to hold context, small enough
      to stay within embedding model limits and stay relevant
    - overlap=50 words: prevents losing context at chunk boundaries
    - source tag: lets us know which dataset a chunk came from
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)

        chunks.append({
            "text": chunk_text_str,
            "source": source,
            "start_word": start,
            "end_word": end,
            "chunk_id": len(chunks)
        })

        start += chunk_size - overlap  # move forward with overlap

    return chunks


def chunk_all(csv_text, pdf_text):
    """Chunk both datasets and combine."""
    print("Chunking elections data...")
    csv_chunks = chunk_text(csv_text, chunk_size=500, overlap=50, source="elections")

    print("Chunking budget PDF...")
    pdf_chunks = chunk_text(pdf_text, chunk_size=500, overlap=50, source="budget")

    all_chunks = csv_chunks + pdf_chunks

    print(f"Total chunks: {len(all_chunks)} "
          f"({len(csv_chunks)} elections + {len(pdf_chunks)} budget)")
    return all_chunks


if __name__ == "__main__":
    # Test chunking
    with open("data/clean_elections.txt", "r", encoding="utf-8") as f:
        csv_text = f.read()
    with open("data/clean_budget.txt", "r", encoding="utf-8") as f:
        pdf_text = f.read()

    chunks = chunk_all(csv_text, pdf_text)

    # Show sample
    print("\n--- Sample chunk (elections) ---")
    print(chunks[0]["text"][:300])
    print("\n--- Sample chunk (budget) ---")
    print(chunks[len(chunks)//2]["text"][:300])