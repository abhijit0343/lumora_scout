<div align="center">

# Lumora Scout

**Two sites enter. One verdict leaves.**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Vite](https://img.shields.io/badge/Vite-5.4+-646CFF.svg)](https://vitejs.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL-black.svg)](https://threejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Overview

**Lumora Scout** is an autonomous agentic intelligence engine that compares two websites or two products across websites by their deepest capabilities. Featuring multi-agent parallel web extraction, human-in-the-loop (HITL) checkpoints, real-time Server-Sent Events (SSE) streaming, local hybrid RAG with EmbeddingGemma 2, and a hardened 4-layer safety guardrail pipeline.

<!-- Demo Placeholder -->
<div align="center">
  <img src="https://via.placeholder.com/800x400?text=Lumora+Scout+Interactive+3D+Arena+Demo" alt="Lumora Scout Demo Placeholder" width="800"/>
</div>

---

## Feature Matrix

| Feature | Description | Architecture / Stack |
| :--- | :--- | :--- |
| **Agentic Comparison** | Multi-agent state machine orchestrating end-to-end comparative analysis | LangGraph + SQLite Checkpointer |
| **Parallel Extraction** | Simultaneous parallel fan-out scraping and feature extraction for Side A and B | Trafilatura + Playwright Fallback |
| **Human-in-the-Loop** | Checkpoints allowing user confirmation/editing of targets and criteria | Checkpoint A (Targets), Checkpoint B (Criteria) |
| **4-Layer Guardrails** | Defense-in-depth safety covering inputs, URLs/SSRF, content, and outputs | L1 Input, L2 SSRF/URL, L3 Content, L4 Output |
| **Hybrid RAG** | Ingest uploaded documentation to ground capability scoring | FAISS IndexFlatIP + BM25 + EmbeddingGemma 2 |
| **Resilient Gateway** | Automatic fallback chain across multiple AI inference providers | Gemini 3.8 Flash &rarr; Groq &rarr; OpenRouter &rarr; Ollama |
| **Real-Time Streaming** | Live SSE telemetry streaming reasoning tokens, matrix rows, and tool events | FastAPI SSE (`sse-starlette`) |
| **3D Visual Arena** | Futuristic WebGL interface rendering interactive comparison holograms | React + Vite + Three.js |

---

## How It Thinks

Lumora Scout executes comparison requests through a disciplined, self-correcting cognitive pipeline:

```
[User Request] 
      │
      ▼
1. RESOLVE ────────► Identifies canonical entities, homepages, and domain scopes
      │
      ▼
2. YOU CONFIRM ────► Checkpoint A (HITL): You verify or edit target URLs
      │
      ▼
3. GUARD ──────────► L2 URL & SSRF verification (DNS checks, blocklists, Safe Browsing)
      │
      ▼
4. EXTRACT (A ‖ B) ─► Parallel fan-out: Scrapes, screens via L3, and extracts capabilities
      │
      ▼
5. ALIGN ──────────► Reconciles disparate feature taxonomies into unified criteria
      │
      ▼
6. GROUND (RAG) ───► Retrieves document context; grades relevance with retry loop
      │
      ▼
7. VERDICT ────────► L4-screened synthesis of scores, trade-offs, and final recommendation
```

---

## Repository Structure

```
lumora-scout/
├── README.md                      # Project root documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── .editorconfig                  # Editor formatting rules
├── docs/                          # Comprehensive technical specifications
│   ├── ARCHITECTURE.md            # System architecture blueprint
│   ├── AGENT_GRAPH.md             # LangGraph state machine & Mermaid graph
│   ├── STREAMING_AND_HITL.md      # SSE protocol & human-in-the-loop specification
│   ├── GUARDRAILS.md              # 4-layer defense-in-depth security model
│   ├── RAG.md                     # EmbeddingGemma 2 hybrid RAG architecture
│   ├── API_CONTRACT.md            # REST and SSE API specifications
│   ├── MODELS_AND_KEYS.md         # Model catalog and API key management
│   ├── SECURITY.md                # Threat modeling and SSRF defense
│   ├── EVALUATION.md              # Benchmarking and red-team evaluation
│   ├── FRONTEND.md                # React & Three.js UI specification
│   ├── ROADMAP.md                 # Development phases and milestones
│   └── frontend/
│       └── LUMORA_DESIGN_PROMPT.md# Frontend design prompt placeholder
├── backend/
│   ├── README.md                  # Backend setup guide
│   ├── pyproject.toml             # UV / Python dependencies (Python >=3.12)
│   ├── .python-version            # Python runtime version
│   ├── .env.example               # Backend environment variables template
│   ├── app/
│   │   ├── main.py                # FastAPI application entrypoint
│   │   ├── core/                  # Configuration, logging, errors, rate limits
│   │   ├── api/                   # Dependencies, SSE transport, route endpoints
│   │   ├── schemas/               # Pydantic state, event, and request models
│   │   ├── llm/                   # LLM clients, fallback chain, structured output
│   │   │   └── prompts/           # Cognitive prompts (router, verdict, etc.)
│   │   ├── agents/                # LangGraph state, workflow graph, node workers
│   │   ├── tools/                 # Scrapers, web search, app stores, GitHub tools
│   │   ├── rag/                   # Chunking, embeddings, FAISS & BM25 indices
│   │   ├── guardrails/            # 4-layer defensive guardrails and blocklists
│   │   └── persistence/           # SQLite checkpointer, databases, cache
│   ├── data/                      # Uploads, indexes, blocklists, cache (.gitkeep)
│   └── tests/                     # Unit, integration, redteam, eval (.gitkeep)
└── frontend/
    ├── README.md                  # Frontend setup guide
    ├── package.json               # Frontend dependencies & scripts
    ├── vite.config.js             # Vite configuration
    ├── .env.example               # Frontend environment template
    └── src/                       # React components, pages, hooks, 3D scenes (.gitkeep)
```

---

## Quick Start

### 1. Environment Configuration

Clone the repository and set up environment variables:

```bash
# Copy backend environment template
cp backend/.env.example backend/.env

# Copy frontend environment template
cp frontend/.env.example frontend/.env
```

Edit `backend/.env` with your API credentials (refer to [MODELS_AND_KEYS.md](docs/MODELS_AND_KEYS.md) for free-tier instructions).

### 2. Backend Setup (`uv`)

```bash
cd backend

# Create virtual environment and install dependencies
uv venv
uv pip sync pyproject.toml

# Start the FastAPI server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000` (docs at `/docs`).

### 3. Frontend Setup (`npm`)

```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

The user interface will be accessible at `http://localhost:5173`.

---

## Roadmap

Unbuilt features and upcoming milestones:

- [ ] **Phase 2**: Full LangGraph node worker implementations and tool scrapers.
- [ ] **Phase 3**: EmbeddingGemma 2 RAG vector and lexical indexing pipeline.
- [ ] **Phase 4**: Interactive Three.js 3D WebGL capability comparison arena.
- [ ] **Phase 5**: Multimodal vision analysis comparing UI screenshots via Playwright.
- [ ] **Phase 6**: Enterprise workspace collaboration and scheduled comparison tracking.

---

## License

This project is licensed under the [MIT License](LICENSE).
