# Name: Kofi Appiah
# Index: 10022300106
# File: rag/prompt.py
# Purpose: Prompt templates with hallucination control and context injection

MAX_CONTEXT_WORDS = 600


def build_context(retrieved_chunks):
    """
    Select and truncate chunks to fit context window.
    Ranks by score, truncates if too long.
    """
    context_parts = []
    word_count = 0

    for i, result in enumerate(retrieved_chunks):
        chunk_text = result["chunk"]["text"]
        source = result["chunk"]["source"]
        score = result["score"]
        words = chunk_text.split()

        if word_count + len(words) > MAX_CONTEXT_WORDS:
            # Truncate this chunk to fit remaining space
            remaining = MAX_CONTEXT_WORDS - word_count
            if remaining > 50:  # only add if meaningful
                chunk_text = " ".join(words[:remaining]) + "..."
                context_parts.append(
                    f"[Source {i+1}: {source} | score: {score:.3f}]\n{chunk_text}"
                )
            break

        context_parts.append(
            f"[Source {i+1}: {source} | score: {score:.3f}]\n{chunk_text}"
        )
        word_count += len(words)

    return "\n\n".join(context_parts)


def build_prompt(query, retrieved_chunks, version="v1"):
    """
    Build the final prompt to send to the LLM.
    Two versions to compare for Part C experiments.
    """
    context = build_context(retrieved_chunks)

    if version == "v1":
        # Basic prompt
        prompt = f"""You are a helpful assistant for Academic City University.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""

    elif version == "v2":
        # Improved prompt with stricter hallucination control
        prompt = f"""You are a knowledgeable assistant for Academic City University.
Your job is to answer questions about Ghana's election results and the 2025 budget.

STRICT RULES:
- Answer ONLY using the provided context
- If the context does not contain the answer, respond: "The available data does not contain information about this."
- Do not make up numbers, names, or facts
- Be concise and specific
- If quoting numbers or names, mention which source they came from

Context:
{context}

Question: {query}

Answer (based strictly on context above):"""

    return prompt, context


if __name__ == "__main__":
    # Test with dummy data
    dummy_results = [
        {
            "chunk": {
                "text": "Year: 2020, Region: Ashanti, Candidate: Nana Akufo-Addo, Party: NPP, Votes: 145584",
                "source": "elections",
                "chunk_id": 0
            },
            "score": 0.92,
            "method": "hybrid"
        }
    ]

    query = "Who won the 2020 election in Ashanti?"

    print("=== PROMPT V1 ===")
    prompt_v1, _ = build_prompt(query, dummy_results, version="v1")
    print(prompt_v1)

    print("\n=== PROMPT V2 ===")
    prompt_v2, _ = build_prompt(query, dummy_results, version="v2")
    print(prompt_v2)