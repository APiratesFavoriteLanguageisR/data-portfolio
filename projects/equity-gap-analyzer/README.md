# Equity Gap Analyzer: Multi-Agent System

> View the full interactive notebook on [Kaggle](https://www.kaggle.com/code/roberttapia001/agents-capstone)

> Read the full project write-up on [Kaggle](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/new-writeup-1764610500333)

> **Note:** This notebook is designed to run in a Kaggle environment. It requires a Google API key stored as a Kaggle secret (`GOOGLE_API_KEY`) and uses the [Students Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) dataset available on Kaggle. For the full interactive experience, run it directly on Kaggle.

---

## Overview

This Google 5-day Generative AI Agents course capstone project implements an Equity Gap Analyzer as a multi-agent system that identifies and explains differences in student outcomes across demographic subgroups. Built using the Google AI Developer Kit (ADK) and Gemini 2.5 Flash, the system analyzes the public StudentsPerformance dataset to surface equity gaps in math, reading, and writing scores across subgroups such as gender, race/ethnicity, parental education level, lunch status, and test preparation course completion. The system produces structured, human-readable equity reports suitable for school leaders and education researchers.

---

## Agent Architecture

The system uses four specialized agents orchestrated by a central coordinator:

| Agent | Role |
|---|---|
| `CoordinatorAgent` | Entry point that interprets the user mission, selects outcome and subgroup columns, and orchestrates the other agents |
| `DataQualityAgent` | Profiles the dataset for missingness, subgroup counts, and small group flags before analysis begins |
| `AnalystAgent` | Computes per-subgroup descriptive statistics, pairwise gaps, and pooled effect sizes relative to a reference group |
| `WriterAgent` | Produces a concise, formatted equity report with a markdown table, effect size interpretation, recommended next steps, and data limitations |

An `InsightsAgent` supplements the pipeline with Gemini-generated, research-informed intervention strategies tailored to the subgroup type and outcome.

---

## Key Features

- **Multi-agent orchestration** — four specialized agents coordinated via Google ADK's `LlmAgent`, `AgentTool`, and `Runner`
- **Data quality profiling** — flags missingness rates and small subgroup counts before analysis runs
- **Effect size calculation** — computes pooled Cohen's d effect sizes for all pairwise subgroup comparisons
- **Research-informed insights** — uses Gemini to surface evidence-based intervention strategies for each equity gap
- **Structured equity reports** — WriterAgent produces formatted markdown reports with tables, narrative interpretation, and actionable next steps
- **User memory** — tracks preferred outcome and subgroup columns across runs for continuity
- **Run logging** — maintains a timestamped log of all missions and report previews for observability
- **Session management** — uses `InMemorySessionService` for stateful multi-turn agent execution

---

## Tech Stack

- **Python** — core language
- `google-adk` — Google AI Developer Kit for multi-agent orchestration (`LlmAgent`, `AgentTool`, `Runner`, `InMemorySessionService`)
- `google-genai` — Gemini API for agent reasoning and research insight generation (`gemini-2.5-flash`)
- `pandas` / `numpy` — data processing, subgroup aggregation, and effect size computation
- `kaggle_secrets` — secure API key handling in the Kaggle environment

---

## How to Run

1. Open the notebook on [Kaggle](https://www.kaggle.com/code/roberttapia001/agents-capstone)
2. Add the [Students Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) dataset via the Data menu
3. Store your Google API key as a Kaggle secret named `GOOGLE_API_KEY`
4. Run all cells in order
5. The final cell runs the coordinator agent with a sample mission. Modify the mission text to analyze different outcome and subgroup combinations

---

## Example Mission

```python
mission = "Analyze reading_score equity gaps by race_ethnicity and produce an interpretable equity report."
```

The system will automatically profile the data, compute subgroup statistics, retrieve research insights, and generate a structured report.

---

## Project Structure

```
equity-gap-analyzer/
├── agents-capstone.ipynb    ← full notebook with code and outputs
└── README.md
```

---

## Limitations

- Race and ethnicity groups in the public dataset are anonymized as Group A–E, preventing conclusions about specific named communities
- Statistical analysis focuses on mean differences and effect sizes; future work could incorporate confidence intervals or regression-based adjustment
- Due to free-tier Gemini API rate limits, the notebook demonstrates a limited number of end-to-end runs

---

## Acknowledgments

- StudentsPerformance dataset sourced from [Kaggle](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)
- Agent orchestration and generation powered by Google's Gemini API and ADK (`gemini-2.5-flash`)
- Developed as part of the [Google 5-Day Generative AI Agents Intensive Course](https://www.kaggle.com/learn-guide/5-day-genai) on Kaggle