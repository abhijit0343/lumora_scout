# Lumora Scout - Backend

FastAPI and LangGraph agentic backend managed with `uv`.

## Architecture Overview
- **Agent Coordinator**: LangGraph state machine with SQLite checkpointer (`checkpoints.sqlite`).
- **Resilient LLM Gateway**: Gemini 3.8 Flash primary with Groq, OpenRouter, and Ollama fallback chain.
- **RAG Engine**: Dual FAISS (IndexFlatIP) and Rank-BM25 hybrid retriever powered by EmbeddingGemma 2.
- **Defensive Guardrails**: 4-layer inspection pipeline (L1 Input, L2 URL/SSRF, L3 Scraped Content, L4 Output).
- **Streaming & HITL**: Real-time Server-Sent Events (SSE) with human-in-the-loop checkpoint pause/resume.

## Prerequisites
- Python 3.12+
- `uv` package and project manager

## Quick Start
```bash
# Navigate to backend directory
cd backend

# Create virtual environment and sync dependencies
uv venv
uv pip sync pyproject.toml

# Copy environment template and configure keys
cp .env.example .env

# Run development server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running Tests
```bash
# Run unit tests
uv run pytest tests/unit

# Run guardrails red-team battery
uv run pytest tests/guardrails_redteam
```
