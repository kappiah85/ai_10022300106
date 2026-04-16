# Name: Kofi Appiah
# Index: 10022300106
# File: app.py
# Purpose: Streamlit UI for the RAG chatbot

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.pipeline import run_pipeline

st.set_page_config(
    page_title="Academic City RAG Chatbot",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Academic City RAG Chatbot")
st.caption("Powered by Claude AI | Data: Ghana Elections + 2025 Budget")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    top_k = st.slider("Number of chunks to retrieve", 3, 10, 5)
    method = st.selectbox("Search method", ["hybrid", "vector", "keyword"])
    prompt_version = st.selectbox("Prompt version", ["v2", "v1"])
    st.divider()
    st.markdown("**About**")
    st.markdown("This RAG system queries:")
    st.markdown("- 🗳️ Ghana Election Results")
    st.markdown("- 💰 2025 Ghana Budget Statement")
    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.debug_info = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "debug_info" not in st.session_state:
    st.session_state.debug_info = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if query := st.chat_input("Ask about Ghana elections or the 2025 budget..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Run pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching and generating response..."):
            output = run_pipeline(
                query,
                top_k=top_k,
                prompt_version=prompt_version,
                method=method
            )

        st.markdown(output["answer"])

        # Show retrieved chunks
        with st.expander("📄 Retrieved chunks"):
            for i, r in enumerate(output["results"]):
                st.markdown(f"**[{i+1}] Source:** `{r['chunk']['source']}` | "
                          f"**Score:** `{r['score']:.4f}` | "
                          f"**Method:** `{r['method']}`")
                st.text(r["chunk"]["text"][:300] + "...")
                st.divider()

        # Show final prompt
        with st.expander("🔍 Final prompt sent to LLM"):
            st.code(output["prompt"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": output["answer"]
    })