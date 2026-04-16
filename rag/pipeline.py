# Name: Kofi Appiah
# Index: 10022300106
# File: rag/pipeline.py
# Purpose: Full RAG pipeline - Query → Retrieve → Prompt → LLM → Response

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embedder import load_index
from rag.retriever import retrieve
from rag.prompt import build_prompt

# Load index once at startup
print("Loading index...")
import os
if not os.path.exists("embeddings/faiss.index"):
    print("Index not found, rebuilding...")
    from rag.data_loader import load_data
    from rag.chunker import chunk_all
    from rag.embedder import build_index
    csv_text, pdf_text = load_data()
    chunks_data = chunk_all(csv_text, pdf_text)
    build_index(chunks_data)

index, chunks = load_index()
print("Pipeline ready.")
# Anthropic client
import streamlit as st
api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# Conversation memory (innovation - Part G)
conversation_history = []


def log_to_file(entry):
    """Save each pipeline run to logs/pipeline_log.jsonl"""
    os.makedirs("logs", exist_ok=True)
    with open("logs/pipeline_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_pipeline(query, top_k=5, prompt_version="v2", method="hybrid"):
    """
    Full RAG pipeline with logging at every stage.
    Returns response + all intermediate data for display.
    """
    timestamp = datetime.now().isoformat()
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")

    # ── Stage 1: Retrieval ──────────────────────────────────────
    print(f"\n[Stage 1] Retrieving top-{top_k} chunks ({method} search)...")
    results = retrieve(query, index, chunks, top_k=top_k, method=method)

    print(f"  Retrieved {len(results)} chunks:")
    for i, r in enumerate(results):
        print(f"  [{i+1}] score={r['score']:.4f} source={r['chunk']['source']} method={r['method']}")

    # ── Stage 2: Prompt Construction ────────────────────────────
    print(f"\n[Stage 2] Building prompt (version={prompt_version})...")
    prompt, context = build_prompt(query, results, version=prompt_version)
    print(f"  Prompt length: {len(prompt.split())} words")
    print(f"\n  --- FINAL PROMPT SENT TO LLM ---")
    print(prompt)
    print(f"  --- END PROMPT ---")

    # ── Stage 3: LLM Generation ─────────────────────────────────
    print(f"\n[Stage 3] Sending to Claude API...")

    # Add conversation history for memory (Part G)
    messages = conversation_history + [{"role": "user", "content": prompt}]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=messages
    )

    answer = response.content[0].text

    # Update conversation memory
    conversation_history.append({"role": "user", "content": query})
    conversation_history.append({"role": "assistant", "content": answer})

    # Keep memory to last 6 exchanges
    if len(conversation_history) > 12:
        conversation_history.pop(0)
        conversation_history.pop(0)

    print(f"\n[Stage 4] Response:")
    print(answer)

    # ── Logging ─────────────────────────────────────────────────
    log_entry = {
        "timestamp": timestamp,
        "query": query,
        "method": method,
        "prompt_version": prompt_version,
        "retrieved_chunks": [
            {
                "source": r["chunk"]["source"],
                "score": r["score"],
                "method": r["method"],
                "text_preview": r["chunk"]["text"][:100]
            }
            for r in results
        ],
        "prompt": prompt,
        "response": answer
    }
    log_to_file(log_entry)

    return {
        "query": query,
        "results": results,
        "context": context,
        "prompt": prompt,
        "answer": answer
    }


if __name__ == "__main__":
    # Test the full pipeline
    test_queries = [
        "Who won the 2020 presidential election in Ghana?",
        "What is the 2025 budget allocation for education?",
    ]

    for q in test_queries:
        output = run_pipeline(q)
        print(f"\nFINAL ANSWER: {output['answer']}")
        print("="*60)