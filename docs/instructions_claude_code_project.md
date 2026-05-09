# BI Assessment Agent — Code Project Instructions

## Read this first
If you are missing context about scope, architecture, or decisions:
- Read `docs/project_summary.md` — master reference
- Read `docs/instructions_code_helper.md` — full technical detail
Do not ask Silvia to repeat information that is in those files.

---

## Who you are helping
Silvia — Senior BI Developer. Knows Python, SQL, DAX, Power BI. New to AutoGen, LlamaIndex, Docker. Has ADHD — be concise, lead with code, one thing at a time.

---

## What this project is
A portable Docker-based AI agent that:
1. Reads TMDL/JSON semantic model exports + CSV files
2. Evaluates them against MD knowledge base files (RAG)
3. Outputs a scored Markdown assessment report

---

## Stack
- Python 3.11 · AutoGen · LlamaIndex · OpenAI API · Docker

---

## Folder structure
```
bi-assessment-agent/
├── docs/                    # project_summary.md, instructions
├── inputs/models/           # TMDL / JSON inputs
├── inputs/data/             # CSV inputs
├── inputs/knowledge/        # MD knowledge base (runtime copy)
├── knowledge/               # Master MD files (source of truth)
├── agents/                  # extractor.py · assessor.py · scorer.py
├── output/reports/          # Generated MD reports
├── main.py                  # Entry point
├── config.py                # Keys + paths from .env
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Coding rules
- Type hints + docstrings on every function
- No global state — pass config explicitly
- Fail loudly — raise with clear messages
- Simple and readable — Silvia maintains this alone
- Nothing requires manual steps inside Docker

---

## Current phase
Check `docs/project_summary.md` → Section 9 (Phased Delivery Plan) for what's done and what's next.

---

## Response rules
- Code first, explanation after
- Bullet points over paragraphs
- One file or function at a time unless asked for more
- If a decision is needed → flag it, give a recommendation, move on
- Never repeat context already in the docs
