# Product Roadmap

## Metadata
- **Purpose**: Defines development milestones, upcoming releases, and future capabilities for Lumora Scout.
- **Scope**: Core framework evolution, multimodal expansion, 3D enhancements, and enterprise scaling.
- **Owner files**: Project backlog and tracking specifications.

---

## 1. Development Milestones Outline

### Phase 1: Repository Foundation & Scaffolding (Current)
- Complete directory structure, type contracts, environment variables, and configuration templates.
- Complete documentation suite detailing 4-layer guardrails, RAG pipeline, LangGraph state, and API contracts.

### Phase 2: Core Agent Implementation & Scrapers
- Implement LangGraph workflow nodes, SQLite checkpoint persistence, and SSE event streaming.
- Implement resilient tool suite: Tavily web search, Trafilatura static fetcher, and Playwright fallback.
- Integrate 4-layer defensive guardrails (L1 input, L2 URL/SSRF, L3 content, L4 output).

### Phase 3: RAG Engine & EmbeddingGemma 2 Integration
- Build ingestion pipeline for PDF, DOCX, TXT, and Markdown files.
- Implement FAISS IndexFlatIP dense store and Rank-BM25 sparse index with hybrid Reciprocal Rank Fusion.
- Integrate agentic grading and self-correction retry loops.

### Phase 4: Three.js 3D Visual Battle Arena & Frontend
- Develop React + Vite interface with real-time SSE streaming.
- Implement Three.js 3D visual arena depicting comparative capability holograms.
- Implement interactive Human-in-the-Loop review modals for targets and criteria.

### Phase 5: Multimodal & Enterprise Expansion
- Multimodal capability analysis: screenshot comparison via Playwright and vision-capable LLM extractors.
- Enterprise SSO, team workspaces, scheduled comparative tracking, and export to PDF/Markdown reports.
