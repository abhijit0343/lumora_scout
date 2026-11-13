# Resilient LLM Gateway & Cognitive Prompts

## Overview
Lumora Scout implements a resilient LLM gateway that automatically fails over across four AI inference providers to ensure 99.9% uptime. It features configurable reasoning thinking levels and enforces structured JSON outputs.

---

## 📁 File Responsibilities & How They Work

### 1. Resilient Provider Clients
- **`gemini_client.py` (Primary)**:
  - Invokes `gemini-3.8-flash` via `google-genai` / `langchain-google-genai`.
  - Supports configurable thinking levels: `low` for routing/guardrails, `medium` for extraction, and `high` for final verdict synthesis.
- **`groq_client.py` (Fallback 1)**:
  - Ultra-fast fallback running `llama-3.3-70b-versatile` on Groq LPU hardware.
- **`openrouter_client.py` (Fallback 2)**:
  - Secondary fallback providing access to open-weights models.
- **`ollama_client.py` (Fallback 3)**:
  - Local, offline fallback running `qwen2.5:7b` on developer hardware.

### 2. `backend/app/llm/fallback_chain.py`
- **Purpose**: Orchestrates transparent provider failovers.
- **How It Works**:
  - Attempts the primary Gemini call. If a rate limit (HTTP 429), timeout, or service error occurs, it sequentially tries each provider defined in `LLM_FALLBACK_CHAIN=groq,openrouter,ollama`.
  - Logs failover events for observability without failing the user request.

### 3. `backend/app/llm/structured_output.py`
- **Purpose**: Enforces deterministic Pydantic structured output extraction.
- **How It Works**:
  - Uses native LLM function/tool-calling or JSON schema mode to parse LLM responses directly into validated Pydantic models.
  - Includes schema auto-repair to fix minor JSON syntax issues.

---

## 📝 Cognitive Prompts Catalog

All prompts reside in `backend/app/llm/prompts/`:

| Prompt File | Associated Node | Purpose |
| :--- | :--- | :--- |
| **`router.md`** | `resolve` | Classifies comparison query into product categories and determines necessary discovery tools. |
| **`resolver.md`** | `resolve` | Resolves ambiguous names into canonical entities, landing URLs, and catalog definitions. |
| **`extractor.md`** | `fetch_extract` | Analyzes scraped pages to extract structured capability records, status flags, and evidence quotes. |
| **`aligner.md`** | `align` | Reconciles disparate feature lists into a unified, balanced comparison criteria matrix. |
| **`grader.md`** | `rag_ground` | Evaluates whether retrieved document chunks provide sufficient evidence; rewrites queries if not. |
| **`verdict.md`** | `verdict` | Synthesizes scores, trade-offs, and persona recommendations; streams live reasoning tokens. |
| **`guard_classifier.md`**| `guard_in`, `guard_urls` | Fast safety classifier evaluating prompt injections, jailbreaks, and policy compliance. |
