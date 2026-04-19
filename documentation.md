# Project Documentation
**Student:** Kofi Appiah  
**Index:** 10022300106  
**Course:** CS4241 - Introduction to Artificial Intelligence

## What I Built
For this project I built a chatbot that can answer questions about 
Ghana's election results and the 2025 budget. The idea is simple — 
instead of the AI just guessing answers from general knowledge, it 
actually searches through the real data first before responding. 
This is what RAG means.

## The Data

I used two datasets:
- A CSV file with Ghana election results from 2012 to 2020. It had 
  615 rows covering different regions, parties and candidates.
- The 2025 Ghana Budget Statement PDF which was 252 pages long.

### Cleaning
The CSV had some messy formatting so I stripped whitespace and removed 
empty rows. I also converted each row into a readable sentence because 
raw CSV data confuses the AI when it tries to read it.

For the PDF I used a library called PyMuPDF to pull out the text from 
each page. PDFs are annoying to work with because they have a lot of 
random spacing and formatting — I had to clean all that out.

### Chunking
I couldn't feed all the text to the AI at once so I split it into 
chunks. I went with 500 words per chunk and a 50 word overlap between 
chunks. The overlap is important because without it you lose information 
at the edges where one chunk ends and another begins.

This gave me 246 chunks in total — 31 from elections and 215 from 
the budget.

I tested smaller chunks (200 words) and bigger ones (1000 words). 
200 words lost too much context. 1000 words retrieved too much 
irrelevant stuff. 500 felt like the sweet spot.

## How the Search Works

I used two types of search and combined them:

**Vector search** — converts the query and all chunks into numbers 
(embeddings) and finds the chunks with the closest meaning. Good for 
general questions about policy and economics.

**Keyword search (BM25)** — looks for actual matching words. Good for 
specific things like names, numbers and regions.

I combined both into hybrid search because neither works perfectly on 
its own. For example vector search alone kept returning budget results 
when I asked about Ashanti election data — it didn't understand that 
"Ashanti" was a location keyword. Adding BM25 fixed that.

## Prompts

I made two versions of the prompt.

Version 1 is basic — gives Claude the context and asks it to answer.

Version 2 is stricter. I added rules telling Claude not to make up 
answers. If the information isn't in the retrieved chunks it has to 
say so instead of guessing. This made a big difference. Without it 
Claude would sometimes give confident-sounding wrong answers.

## The Pipeline

Here's what happens when you type a question:
1. Your question gets converted into a vector
2. The system searches the 246 chunks using hybrid search
3. The top 5 chunks get added to the prompt
4. The prompt goes to Claude
5. You get the answer back along with the chunks that were used

Everything gets logged to a file so you can see exactly what happened 
at each step.

## Memory

I added a memory feature so the chatbot remembers the conversation. 
If you ask about NPP votes and then say "what about NDC?" it knows 
what you mean. It keeps the last 6 exchanges in memory.

## What Didn't Work Well

The election data doesn't have a column saying who "won" each region 
so questions like "who won Ashanti?" don't always give a clean answer. 
Asking for vote counts works much better.

Also the app sleeps after 7 days of no activity on Streamlit's free 
plan. It wakes up when someone visits but takes a minute or two.