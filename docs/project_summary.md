# BI Assessment Agent — Project Summary
> **Version:** 0.1 — Initial Plan  
> **Author:** Silvia  
> **Status:** Planning phase

---

## 1. Project Overview

A portable AI agent that connects to financial semantic models and data sources, evaluates them against best practice reference documentation, and produces a structured assessment report with scores, gaps, and improvement suggestions.

**Primary use case:** Internal consultancy tool — deployed for client engagements to assess the quality and completeness of financial Power BI semantic models.

**Output:** A Markdown report scoring the model across multiple dimensions, listing gaps, and recommending what is buildable.

---

## 2. Goals

| Goal | Description |
|------|-------------|
| **Assess semantic models** | Parse TMDL/JSON exports and evaluate against financial best practices |
| **Analyse data files** | Accept CSV inputs representing financial data or model exports |
| **RAG over knowledge base** | Use reference MD documents as the agent's knowledge source |
| **Score & report** | Produce a structured, client-ready assessment report |
| **Portable** | Easy to install and run on client environments via Docker |
| **Slim** | Minimal dependencies — no heavy frameworks unless necessary |

---

## 3. Tech Stack

| Layer | Tool | Reason |
|-------|------|--------|
| Language | Python 3.11 | Stable, wide support |
| Orchestration | AutoGen (Microsoft) | Enterprise-friendly, multi-agent support |
| RAG | LlamaIndex | Simple document retrieval, less overhead than LangChain |
| LLM | OpenAI / Azure OpenAI | Client-compatible — Azure preferred for Microsoft environments |
| Containerisation | Docker + docker-compose | Portability — single command deploy |
| Output format | Markdown | Simple, v1 — HTML upgrade in v2 |

---

## 4. Inputs

| Input Type | Format | Source |
|-----------|--------|--------|
| Semantic model | TMDL or JSON export | Power BI Desktop export or manual |
| Financial data | CSV | Client data extracts |
| Knowledge base | Markdown files | Reference docs (see Section 6) |

> **Not in scope for v1:** Live Power BI Desktop connection, API calls to Power BI Service, Excel files

---

## 5. Architecture

```
INPUT LAYER
  ├── inputs/models/       ← TMDL / JSON semantic model exports
  ├── inputs/data/         ← CSV files
  └── inputs/knowledge/    ← MD reference documents

PROCESSING LAYER
  ├── extractor.py         ← Parses model + CSV into structured text
  ├── assessor.py          ← RAG agent — compares model vs knowledge base
  └── scorer.py            ← Scores gaps, produces structured findings

OUTPUT LAYER
  └── output/reports/      ← Generated Markdown assessment report
```

### Agent Flow

```
1. User places files in inputs/
2. Extractor parses TMDL/JSON + CSVs → structured text
3. Knowledge base (MD files) → chunked + embedded → vector store
4. Assessor agent → retrieves relevant reference chunks → compares vs model
5. Scorer agent → produces gap scores per dimension
6. Report generator → writes Markdown report to output/reports/
```

---

## 6. Project Folder Structure

```
bi-assessment-agent/
│
├── inputs/
│   ├── models/                          # TMDL or JSON semantic model exports
│   ├── data/                            # CSV files
│   └── knowledge/                       # MD knowledge base files
│
├── knowledge/                           # Master copies of reference MDs
│   ├── financial_terms.md
│   ├── best_practices_semantic_models.md
│   └── financial_model_standards.md
│
├── agents/
│   ├── extractor.py                     # Input parser
│   ├── assessor.py                      # RAG assessment agent
│   └── scorer.py                        # Scoring + gap analysis agent
│
├── output/
│   └── reports/                         # Generated assessment reports
│
├── main.py                              # Entry point
├── config.py                            # API keys, model config
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container definition
└── docker-compose.yml                   # Volume mounts + env vars
```

---

## 7. Knowledge Base Documents

| File | Purpose | Status |
|------|---------|--------|
| `financial_terms.md` | Financial terminology, measure names, DB table names | ✅ v1 draft complete |
| `best_practices_semantic_models.md` | Naming conventions, DAX patterns, relationships, performance, security | ✅ v1 draft complete |
| `financial_model_standards.md` | Required subject areas, account hierarchy, P&L/BS/CF structure, dimensions, buildable reports | ✅ v1 draft complete |

> All three are placeholders. Final versions to be reviewed and expanded before production use.

---

## 8. Assessment Report Structure (Output)

Each generated report will contain:

```
# Assessment Report — [Model Name] — [Date]

## Executive Summary
- Overall score
- Top 3 gaps
- Top 3 opportunities

## Scores by Dimension
- Schema & Structure        [score /10]
- Measure Completeness      [score /10]
- Naming Conventions        [score /10]
- Time Intelligence         [score /10]
- Budget & Variance         [score /10]
- Security                  [score /10]
- Data Quality (CSV)        [score /10]

## Gaps Found
- [Severity] Description of gap + which best practice it violates

## Suggestions for Improvement
- Prioritised list of fixes

## What Is Buildable
- Reports / analyses that can be created with the current model
- Reports / analyses blocked by missing components
```

---

## 9. Phased Delivery Plan

### Phase 1 — Foundation (current)
- [x] Define scope and architecture
- [x] Create knowledge base MD placeholders (3 files)
- [ ] Set up project folder structure
- [ ] `requirements.txt`, `Dockerfile`, `docker-compose.yml`
- [ ] `config.py` — API key management

### Phase 2 — Extraction
- [ ] `extractor.py` — parse TMDL/JSON model exports
- [ ] `extractor.py` — parse CSV files
- [ ] Unit tests for extractor

### Phase 3 — RAG & Assessment
- [ ] Chunk + embed knowledge base MDs (LlamaIndex)
- [ ] `assessor.py` — retrieval + comparison agent (AutoGen + LlamaIndex)
- [ ] Prompt engineering for assessment logic

### Phase 4 — Scoring & Reporting
- [ ] `scorer.py` — gap scoring per dimension
- [ ] Report generator → Markdown output
- [ ] End-to-end test with sample model

### Phase 5 — Packaging & Polish
- [ ] Docker build + test
- [ ] `docker-compose.yml` volume mounts
- [ ] README with install + usage instructions
- [ ] Sample inputs for demo

### Phase 6 — V2 Considerations (future)
- [ ] HTML report output
- [ ] Live Power BI Desktop connection (pbi-cli integration)
- [ ] Azure OpenAI support
- [ ] Web UI for non-technical users

---

## 10. Open Decisions

| Decision | Options | Status |
|----------|---------|--------|
| LLM provider for v1 | OpenAI API vs Azure OpenAI | ⏳ To decide |
| Vector store | In-memory (LlamaIndex default) vs ChromaDB | ⏳ To decide |
| Report format v2 | HTML vs PDF | ⏳ Future |
| Auth / API key handling | `.env` file vs Docker secrets | ⏳ To decide |

---

## 11. Reference Repositories Analysed

| Repo | What we borrowed |
|------|-----------------|
| `lentomurri/pbi-cli` | TMDL export approach, model serialisation pattern |
| `AI4Finance-Foundation/FinRobot` | Multi-agent pipeline pattern, specialised agent roles, report generation approach |
