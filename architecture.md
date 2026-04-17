# System Architecture — Academic City RAG Chatbot
**Student:** Kofi Appiah  
**Index:** 10022300106

## Data Flow
1. User types a query in the Streamlit UI
2. Query is embedded using sentence-transformers (MiniLM-L6-v2)
3. Hybrid search runs — FAISS vector search + BM25 keyword search
4. Top-5 chunks retrieved and ranked by score
5. Chunks injected into prompt template (V1 or V2)
6. Final prompt sent to Claude API
7. Response returned and displayed with retrieved chunks and prompt

## Components Interaction

| Component | Input | Output |
|---|---|---|
| data_loader.py | Raw CSV + PDF | Cleaned text files |
| chunker.py | Cleaned text | 246 overlapping chunks |
| embedder.py | Chunks | FAISS index + embeddings |
| retriever.py | Query + index | Top-k ranked chunks |
| prompt.py | Query + chunks | Final prompt string |
| pipeline.py | Query | Full RAG response + logs |
| app.py | User input | Chat UI response |

## Design Justification

1. **Hybrid search** — Election data has specific names and numbers
   (keyword search excels here) while budget data has semantic meaning
   (vector search excels here). Hybrid covers both.

2. **Chunk size 500 words** — Election rows are short so small chunks
   preserve row integrity. Budget paragraphs are longer so 500 words
   captures full policy context.

3. **Hallucination control** — Ghana-specific data requires accuracy.
   Prompt V2 strictly limits answers to retrieved context, preventing
   the model from inventing figures or election results.

4. **Memory-based RAG** — Conversation history allows follow-up questions
   like "what about NDC?" after asking about NPP, making the chatbot
   more natural to use.

5. **FAISS vector store** — Efficient similarity search at low cost,
   suitable for a student project with 246 vectors.