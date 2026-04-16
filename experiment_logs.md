# Manual Experiment Logs
**Student:** Kofi Appiah  
**Index:** 10022300106  
**Date:** 19th April 2026  

---

## Experiment 1 — Chunking Strategy Comparison

**Objective:** Compare chunk sizes and their effect on retrieval quality.

| Chunk Size | Overlap | Chunks Created | Retrieval Quality |
|---|---|---|---|
| 200 words | 20 | 580+ | Too granular, loses context |
| 500 words | 50 | 246 | Best balance of context and precision |
| 1000 words | 100 | 130 | Too broad, irrelevant info retrieved |

**Conclusion:** 500 words with 50 overlap gave the best retrieval results.

---

## Experiment 2 — Prompt Version Comparison

**Query:** "What is the NPP votes in Brong Ahafo region?"

**Prompt V1 Response:**
- Gave answer but sometimes added extra unverified context
- Less strict about staying within retrieved data

**Prompt V2 Response:**
- Strictly used only retrieved context
- Broke down votes by Bono, Bono East and Ahafo regions
- Cited exact figures: 292,604 (58.23%), 199,720 (42.33%), 145,584 (55.04%)

**Conclusion:** Prompt V2 produced more accurate, source-grounded responses.

---

## Experiment 3 — Search Method Comparison

**Query:** "NDC votes in Accra"

| Method | Top Result Source | Score | Quality |
|---|---|---|---|
| Vector only | budget | 0.312 | Wrong — returned budget data |
| Keyword only | elections | 11.94 | Correct — returned election data |
| Hybrid | elections | 11.94 | Correct — best of both methods |

**Conclusion:** Hybrid search outperforms vector-only for specific keyword queries.

---

## Experiment 4 — Failure Case Analysis

**Query:** "Who won the 2020 presidential election in Ghana?"

**Result:** System returned budget context instead of election winner.

**Why it failed:** The elections CSV contains regional data but no clear "winner" 
column. The retriever couldn't find a direct answer.

**Fix applied:** Improved chunking to include more context per row so the 
model can infer results from vote percentages.

---

## Experiment 5 — Adversarial Query Testing (Part E)

### Adversarial Query 1 — Ambiguous
**Query:** "What happened in 2020?"

**RAG Response:** Retrieved election data from 2020 but couldn't determine 
what specific event the user meant.

**Pure LLM Response (no retrieval):** Gave general world events for 2020 
including COVID-19 — completely unrelated to the dataset.

**Conclusion:** RAG system stayed on topic; pure LLM hallucinated irrelevant content.

---

### Adversarial Query 2 — Misleading
**Query:** "How much money did Ghana make in 2025?"

**RAG Response:** Said the data does not contain total revenue figures, 
but provided related budget allocation figures.

**Pure LLM Response:** Made up a specific GDP figure with no source.

**Conclusion:** RAG system correctly refused to fabricate; pure LLM hallucinated.

---

## Overall Findings

- Hybrid search consistently outperformed single-method retrieval
- Prompt V2 reduced hallucination rate significantly
- RAG system was more reliable than pure LLM for domain-specific queries
- Main weakness: election data lacks explicit "winner" field