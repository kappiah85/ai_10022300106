# Part B & E — Evaluation Evidence
**Student:** Kofi Appiah
**Index:** 10022300106

---

# PART B — Retrieval Failure Cases & Fixes

## Failure Case 1 — Wrong source retrieved

**Query:** "Who won in Ashanti?"

**Expected:** Election data from Ashanti region

**Actual retrieval result:**
- Source: budget | Score: 0.312
- Retrieved budget text about sports development
- WRONG — returned budget chunks instead of election data

**Why it failed:**
The query "who won" is semantically closer to budget 
language than election CSV rows which contain structured 
data like "Year, Region, Candidate, Votes"

**Fix implemented:**
Switched from pure vector search to hybrid search.
BM25 keyword component picks up "Ashanti" as a keyword
and correctly retrieves election chunks.

**After fix result:**
- Source: elections | Score: 11.94
- Correctly retrieved Ashanti region election data

---

## Failure Case 2 — Ambiguous query retrieves wrong chunks

**Query:** "What happened in 2020?"

**Actual retrieval result:**
- Source: budget | Score: 4.2
- Retrieved budget text mentioning 2020 financial data
- WRONG — user likely meant 2020 elections

**Why it failed:**
"2020" appears many times in budget document so 
keyword search pulls budget chunks. Query too vague.

**Fix implemented:**
Prompt V2 tells Claude to say "data does not contain 
information" rather than hallucinating an answer.
User is guided to ask more specific questions.

---

# PART E — RAG vs Pure LLM Comparison

## Test 1 — Adversarial Query: Ambiguous

**Query:** "What happened in Ghana recently?"

### RAG System Response:
"The available data does not contain information about 
this. The provided context includes 2020 election results 
and 2025 budget allocations but does not cover recent events."

### Pure LLM Response (no retrieval):
"Recently in Ghana, there have been various political 
and economic developments including elections and 
infrastructure projects..." 
[makes up general statements with no source]

**Analysis:**
- RAG: Honest, stayed on topic, no hallucination ✅
- Pure LLM: Fabricated general statements, no evidence ❌
- RAG wins on accuracy and honesty

---

## Test 2 — Adversarial Query: Misleading

**Query:** "Ghana has no election data before 2020, correct?"

### RAG System Response:
"The available data does not confirm this. The provided 
context contains election results from 2012 and 2016 
in addition to 2020 data."

### Pure LLM Response (no retrieval):
"You are correct that comprehensive digital election 
records in Ghana primarily start from 2020..."
[agrees with false premise]

**Analysis:**
- RAG: Correctly contradicted the false premise ✅
- Pure LLM: Agreed with misleading statement ❌
- RAG wins on factual accuracy

---

## Summary Comparison Table

| Metric | RAG System | Pure LLM |
|---|---|---|
| Hallucination rate | Low — refuses to invent | High — makes up answers |
| Domain accuracy | High — uses actual data | Low — uses general knowledge |
| Source transparency | Shows retrieved chunks | No sources shown |
| Handles ambiguity | Says "not in data" | Makes up plausible answer |
| Consistency | Same answer every time | Varies between runs |

**Conclusion:** RAG system significantly outperforms pure LLM 
for domain-specific queries about Ghana elections and budget.
Evidence shows RAG reduces hallucination and improves accuracy.