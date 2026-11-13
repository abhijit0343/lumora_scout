# Lumora Scout - Master Documentation Hub

Welcome to the comprehensive technical documentation for **Lumora Scout**, an agentic AI intelligence engine that compares two websites or two products across websites by their deepest capabilities, with human-in-the-loop (HITL) checkpoints, real-time Server-Sent Events (SSE) streaming, local hybrid RAG with EmbeddingGemma 2, and 4-layer defense-in-depth safety guardrails.

---

## 📚 Documentation Catalog

This documentation suite details every subsystem, file responsibility, cognitive prompt, and workflow lifecycle.

| Document | Focus Area | Key Files Documented |
| :--- | :--- | :--- |
| **[`RAG_SYSTEM.md`](RAG_SYSTEM.md)** | Document ingestion, dual FAISS/BM25 indexing, EmbeddingGemma 2 embeddings, similarity math, agentic self-correction loop | `app/rag/*.py`, `app/agents/nodes/rag_ground.py` |
| **[`GUARDRAILS_SYSTEM.md`](GUARDRAILS_SYSTEM.md)** | 4-layer defense-in-depth security model: L1 Input, L2 URL/SSRF, L3 Content, L4 Output, Safe Browsing, Blocklists | `app/guardrails/*.py`, `app/agents/nodes/guard_*.py` |
| **[`AGENT_GRAPH_SYSTEM.md`](AGENT_GRAPH_SYSTEM.md)** | LangGraph state machine, state schema, 11 workflow nodes, parallel extraction fan-out, routing logic | `app/agents/*.py`, `app/agents/nodes/*.py` |
| **[`TOOLS_AND_SCRAPERS.md`](TOOLS_AND_SCRAPERS.md)** | Web search (Tavily/Brave), static scraping (Trafilatura), headless browser (Playwright), App Stores, GitHub, TMDB | `app/tools/*.py` |
| **[`LLM_AND_PROMPTS.md`](LLM_AND_PROMPTS.md)** | Resilient LLM fallback gateway (Gemini -> Groq -> OpenRouter -> Ollama), structured JSON parsing, prompt catalog | `app/llm/*.py`, `app/llm/prompts/*.md` |
| **[`API_AND_STREAMING.md`](API_AND_STREAMING.md)** | FastAPI routes, SSE streaming protocol (10 event types), HITL checkpoints (A, B, C), session state recovery | `app/api/*.py`, `app/schemas/*.py` |
| **[`PERSISTENCE_AND_CACHE.md`](PERSISTENCE_AND_CACHE.md)**| SQLite LangGraph checkpointer, document catalog database, search and scraper caching layers | `app/persistence/*.py` |
| **[`FRONTEND_AND_3D.md`](FRONTEND_AND_3D.md)** | React + Vite UI architecture, Three.js 3D comparison arena, live SSE streaming telemetry hooks | `frontend/src/*`, `docs/frontend/*` |

---

## 🔄 End-to-End Cognitive Architecture

The diagram below illustrates how all components, files, and guardrail layers collaborate during a comparative analysis session:

```
[User Request: Compare Site A vs Site B]
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Layer 1 Guardrail (input_guard.py + injection_guard.py) │ ──► [Fail: Terminate with blocked event]
 └─────────────────────────────────────────────────────────┘
                      │ Pass
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Entity Resolution (resolve.py + router.md + resolver.md)│ ──► [Tools: web_search.py]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Checkpoint A: Human Confirmation (confirm_targets.py)   │ ──► [HITL Interrupt: Verify/Edit URLs]
 └─────────────────────────────────────────────────────────┘
                      │ User Approves / Resumes
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Layer 2 Guardrail (url_guard.py + ssrf_guard.py)        │ ──► [Redirects, Safe Browsing, SSRF IP Blocks]
 └─────────────────────────────────────────────────────────┘
                      │ Safe
                      ▼
            PARALLEL FAN-OUT EXTRACTION
            ┌───────────────────────────┐
            │ fetch_extract.py (Side A) │ ──► [fetch_page.py / playwright_fetch.py]
            │                           │ ──► [Layer 3 Guardrail: content_guard.py]
            │                           │ ──► [LLM Extractor: extractor.md]
            └─────────────┬─────────────┘
                          │
            ┌─────────────┴─────────────┐
            │ fetch_extract.py (Side B) │ ──► [fetch_page.py / playwright_fetch.py]
            │                           │ ──► [Layer 3 Guardrail: content_guard.py]
            │                           │ ──► [LLM Extractor: extractor.md]
            └─────────────┬─────────────┘
                          │
                          ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Criteria Alignment (align.py + aligner.md)              │ ──► [Reconcile feature taxonomies]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Checkpoint B: Criteria Review (confirm_criteria.py)     │ ──► [Optional HITL Interrupt]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ RAG Grounding Loop (rag_ground.py + hybrid_retriever.py)│ ──► [FAISS + BM25 + EmbeddingGemma 2]
 │                                                         │ ──► [grader.md -> Rewrite query up to 2x]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Quantitative Scoring (score.py + similarity.py)         │ ──► [Top-K mean cosine similarity]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Executive Verdict (verdict.py + verdict.md)             │ ──► [Streaming reasoning tokens via SSE]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Layer 4 Guardrail (output_guard.py)                     │ ──► [PII scrubbing, secret leak prevention]
 └─────────────────────────────────────────────────────────┘
                      │
                      ▼
       [Terminal SSE 'done' Event Emitted]
```

---

## 🛠️ Global Dependency Management

All backend Python dependencies are managed through two synchronized interfaces:
1. **Modern UV Toolchain**: `backend/pyproject.toml`
2. **Global Pip Requirements**: `requirements.txt` (at root) & `backend/requirements.txt`

To install all dependencies globally or into an active virtual environment:
```powershell
pip install -r requirements.txt
```
