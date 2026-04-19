# Academic City RAG Chatbot

**Student Name:** Kofi Appiah
**Index Number:** 10022300106
**Course:** CS4241 - Introduction to Artificial Intelligence
**Lecturer:** Godwin N. Danso
**Date:** 19th April 2026

## Live Demo
[Click here to use the chatbot](https://ai10022300106-kvexvt6aavkquax5nkmkcb.streamlit.app)

## GitHub Repository
[https://github.com/kappiah85/ai_10022300106](https://github.com/kappiah85/ai_10022300106)

## Project Overview
A RAG chatbot built for Academic City University. Allows users to query Ghana Election Results and the 2025 Ghana Budget Statement using natural language, powered by Claude AI.

## Datasets Used
- Ghana Election Results CSV (615 rows, 2012-2020)
- 2025 Ghana Budget Statement PDF (252 pages)

## Tech Stack
- LLM: Anthropic Claude (claude-haiku-4-5-20251001)
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector Store: FAISS
- Keyword Search: BM25 (rank-bm25)
- UI: Streamlit
- Deployment: Streamlit Cloud

## RAG Pipeline
User Query -> Hybrid Search (Vector + BM25) -> Context Selection -> Prompt -> Claude API -> Response

## Key Design Decisions
1. Hybrid search combines FAISS vector search and BM25 keyword search
2. Chunk size 500 words with 50 word overlap
3. Prompt V2 strict hallucination control
4. Memory-based RAG for conversation history
5. FAISS vector store for efficient local similarity search

## Sample Questions
- Nana Akufo-Addo votes in Ashanti region
- GH¢ allocation sanitary pads 2025
- capitation grant 2025 budget
- NPP votes Bono region 2020

## How to Run Locally
git clone https://github.com/kappiah85/ai_10022300106.git
cd ai_10022300106
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
