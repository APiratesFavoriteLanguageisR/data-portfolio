# GenAI Capstone: Academic Research Assistant

> View the full interactive notebook on [Kaggle](https://www.kaggle.com/code/roberttapia001/genai-capstone-academic-assistant)

> **Note:** This notebook is designed to run in a Kaggle environment. It requires a Google API key stored as a Kaggle secret (`GOOGLE_API_KEY`) and uses the [arXiv dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) available on Kaggle. For the full interactive experience, run it directly on Kaggle.

---

## Overview

This Google 5-day Generative AI course capstone project demonstrates a Retrieval-Augmented Generation (RAG) system that retrieves relevant documents and generates answers using a large language model. The RAG system uses the arXiv dataset, which is hosted on Kaggle, as well as the Gemini 1.5 Flash model, and was created to help a user research topics without having to wade through pages and pages of non-relevant information. Beyond basic retrieval, the assistant supports multi-turn conversation memory, three response tone presets (academic, friendly, and critical), and an automated evaluation pipeline that scores each response on relevance, grounding, and clarity using structured JSON output from Gemini.

---

## Key Features

- **RAG Pipeline** — academic abstracts are chunked, embedded, and retrieved using cosine similarity to ground responses in relevant source material
- **Gemini Embeddings** — uses `models/embedding-001` to convert text chunks and user queries into 768-dimensional semantic vectors
- **Tone Control** — users can select academic, friendly, or critical response styles before starting a session
- **Multi-Turn Memory** — the `ResearchAgent` class retains recent conversation history for contextual follow-up questions
- **Automated Evaluation** — each response is optionally scored on relevance, grounding, and clarity (1–5) using structured JSON output from Gemini
- **Score Explanation** — Gemini provides plain-language reasoning behind each evaluation score
- **Session Summary** — at the end of a session, Gemini summarizes the full conversation and displays average evaluation scores
- **Suggested Questions** — users can type "help" to receive AI-generated example questions based on sampled abstracts

---

## Tech Stack

- **Python** — core language
- `google-generativeai` — Gemini API for embeddings, generation, and evaluation
- `pandas` / `numpy` — data processing and embedding matrix operations
- `sklearn.metrics.pairwise` — cosine similarity for vector search
- `tqdm` — progress tracking during embedding generation
- `re` / `json` — structured output parsing from Gemini responses
- `kaggle_secrets` — secure API key handling in the Kaggle environment
- `IPython.display` — enhanced markdown rendering in notebook output

---

## How to Run

1. Open the notebook on [Kaggle](https://www.kaggle.com/code/roberttapia001/genai-capstone-academic-assistant)
2. Add the [arXiv dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) to the notebook via the Data menu
3. Store your Google API key as a Kaggle secret named `GOOGLE_API_KEY`
4. Run all cells in order
5. When prompted, uncomment `run_chat(agent)` in the final cell to launch the assistant

---

## Project Structure

```
rag-research-assistant/
├── genai-capstone-academic-assistant.ipynb    ← full notebook with code and outputs
└── README.md
```

---

## Acknowledgments

- arXiv metadata dataset provided by Cornell University on Kaggle (CC0-1.0 license)
- Embeddings and generation powered by Google's Gemini API (`models/embedding-001` and `models/gemini-1.5-flash`)
- Developed as part of the [Google 5-Day Generative AI Intensive Course](https://www.kaggle.com/learn-guide/5-day-genai) on Kaggle