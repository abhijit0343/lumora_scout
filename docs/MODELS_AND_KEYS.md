# Models and API Keys Configuration

## Metadata
- **Purpose**: Complete catalog of all AI models, external provider APIs, credentials, purpose descriptions, and free-tier allocation guidelines for Lumora Scout.
- **Scope**: Primary LLM, fallback chain models, embedding models, rerankers, search engines, app store scrapers, and observability integrations.
- **Owner files**: `backend/.env.example`, `backend/app/core/config.py`, `backend/app/llm/*`.

---

## 1. Large Language Models (LLMs)

### 1.1 Primary LLM: Google Gemini
- **Model Identifier**: `gemini-3.8-flash` (`LLM_PRIMARY_MODEL`)
- **Provider**: Google AI Studio / Google Cloud
- **Purpose**: Primary comparative reasoning, entity resolution, capability extraction, criteria alignment, and final verdict synthesis.
- **Credential**: `GEMINI_API_KEY`
- **Acquisition**: Obtain from [Google AI Studio](https://aistudio.google.com/).
- **Free Tier**: Generous free-tier requests per minute (RPM) and requests per day (RPD).

### 1.2 Fallback 1: Groq Cloud
- **Model Identifier**: `llama-3.3-70b-versatile` (`GROQ_MODEL`) - *Verify on Groq's models page*
- **Provider**: Groq Cloud Console
- **Purpose**: Ultra-fast fallback inference when primary Gemini calls encounter rate limits or timeouts.
- **Endpoint**: `https://api.groq.com/openai/v1` (`GROQ_BASE_URL`)
- **Credential**: `GROQ_API_KEY`
- **Acquisition**: Obtain from [Groq Console](https://console.groq.com/).
- **Free Tier**: Free developer tier available with per-minute rate limits.

### 1.3 Fallback 2: OpenRouter
- **Model Identifier**: User-selected `:free` model with tool support (`OPENROUTER_MODEL`)
- **Provider**: OpenRouter
- **Purpose**: Secondary cloud fallback providing access to open-weights models.
- **Endpoint**: `https://openrouter.ai/api/v1` (`OPENROUTER_BASE_URL`)
- **Credential**: `OPENROUTER_API_KEY`
- **Acquisition**: Obtain from [OpenRouter](https://openrouter.ai/).
- **Free Tier**: Offers dedicated `:free` model routing endpoints.

### 1.4 Fallback 3: Local Ollama
- **Model Identifier**: `qwen2.5:7b` (`OLLAMA_MODEL`)
- **Provider**: Self-hosted local Ollama daemon
- **Purpose**: Offline, completely local fallback ensuring zero cloud dependency if external APIs are unreachable.
- **Endpoint**: `http://localhost:11434` (`OLLAMA_BASE_URL`)
- **Credential**: None required.
- **Free Tier**: 100% free, runs locally on developer hardware.

---

## 2. Embedding & Reranking Models

### 2.1 Embedding Model: EmbeddingGemma 2
- **Model Identifier**: `google/embeddinggemma-2` (`EMBEDDING_MODEL`)
- **Provider**: Hugging Face Hub / Google
- **Purpose**: Generating 768-dimensional dense vector embeddings for RAG document chunks and search queries.
- **Credential**: `HF_TOKEN` (Optional; required if model repo requires authenticated access).
- **Notes**: *VERIFY ON MODEL CARD* for exact prompt prefixes, instruction formatting, and hardware requirements.

### 2.2 Cross-Encoder Reranker: BGE Reranker
- **Model Identifier**: `BAAI/bge-reranker-v2-m3` (`RERANKER_MODEL`)
- **Provider**: Hugging Face Hub
- **Purpose**: Cross-encoder scoring for candidate retrieval reranking.
- **Credential**: None required (public open-weights model).

---

## 3. Web Search & External Data Tool Credentials

| Key Name | Service / Tool | Purpose | Acquisition & Free Tier |
| :--- | :--- | :--- | :--- |
| `TAVILY_API_KEY` | Tavily AI Search | Clean web research extraction for target products | [Tavily](https://tavily.com/) (1,000 free searches/month) |
| `BRAVE_API_KEY` | Brave Search API | Independent web index search fallback | [Brave Search](https://brave.com/search/api/) (Free tier) |
| `TMDB_API_KEY` | The Movie Database | Metadata extraction for entertainment comparisons | [TMDB](https://www.themoviedb.org/settings/api) (Free API) |
| `OMDB_API_KEY` | Open Movie Database | Film and media rating metadata | [OMDb API](https://www.omdbapi.com/apikey.aspx) (Free tier) |
| `YOUTUBE_API_KEY` | YouTube Data API v3 | Product review videos and transcript discovery | [Google Cloud Console](https://console.cloud.google.com/) |
| `GITHUB_TOKEN` | GitHub REST/GraphQL | Repository metrics (stars, issues, releases, tech stack) | [GitHub Settings](https://github.com/settings/tokens) (Free personal token) |
| `SAFE_BROWSING_API_KEY` | Google Safe Browsing | URL reputation and malware domain filtering | [Google Cloud Console](https://console.cloud.google.com/) (Free quota) |
| `LANGSMITH_API_KEY` | LangSmith | Agent graph tracing and observability | [LangSmith](https://smith.langchain.com/) (Free developer tier) |
