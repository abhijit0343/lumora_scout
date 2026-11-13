# System Architecture

## Metadata
- **Purpose**: High-level structural architectural blueprint of Lumora Scout.
- **Scope**: Backend systems, LangGraph agent coordinator, RAG engine, guardrails stack, and React/Three.js frontend.
- **Owner files**: `backend/app/main.py`, `backend/app/agents/graph.py`, `frontend/src/*`.

---

## 1. Architectural Highlights
- **Decoupled Architecture**: High-performance FastAPI asynchronous backend decoupled from interactive React + Three.js client via Server-Sent Events.
- **Agentic Orchestration**: LangGraph state machine orchestrating multi-phase comparative reasoning with parallel fan-out extraction.
- **Deterministic Checkpointing**: SQLite-backed checkpointer ensuring full session pause/resume capability across Human-in-the-Loop checkpoints.
- **Multi-Layer Defensive Security**: 4-layer guardrail pipeline inspecting inputs, URLs/IPs, scraped contents, and synthesized outputs.
- **Hybrid Retrieval Augmented Generation**: Dual FAISS dense and BM25 sparse index stores with agentic self-correction grading loops.

## 2. Backend Subsystems Outline
- **API Transport Layer (`app/api/`)**: FastAPI routers, dependency injection providers, and Server-Sent Event streaming formatters.
- **Core Orchestration (`app/agents/`)**: State definition, graph edges, conditional routers, parallel fan-out workers, and checkpoint triggers.
- **Resilient LLM Gateway (`app/llm/`)**: Multi-provider fallback chain (Gemini -> Groq -> OpenRouter -> Ollama) with structured Pydantic extraction.
- **External Tools Suite (`app/tools/`)**: Web search (Tavily/Brave), static page scraper (Trafilatura), headless browser (Playwright), GitHub, App Store, and TMDB tools.
- **RAG Engine (`app/rag/`)**: Chunkers, EmbeddingGemma 2 embedders, FAISS vector stores, BM25 indices, and similarity aggregators.
- **Defensive Guardrails (`app/guardrails/`)**: Input, SSRF/URL, scraped content, and output verification filters.
- **Persistence Layer (`app/persistence/`)**: SQLite thread checkpointer, cache engines, and document index stores.

## 3. Frontend Architecture Outline
- **Client Foundation**: React 18 bundled with Vite for near-instant hot module replacement.
- **3D Visualization Arena (`src/three/`)**: Three.js WebGL canvas rendering interactive comparison arenas and capability radar spheres.
- **Streaming State Machine (`src/hooks/`)**: Custom React hooks handling SSE reconnection, incremental token accumulation, and HITL interrupt prompts.
- **Component Hierarchy (`src/components/`)**: Comparison inputs, criteria matrix, live terminal log, and executive verdict viewers.
