# Retrieval-Augmented Generation (RAG) Architecture

## Overview
Lumora Scout incorporates an enterprise-grade, hybrid Retrieval-Augmented Generation (RAG) engine. When users upload proprietary benchmark documents, internal feature requirements, pricing sheets, or RFPs, the RAG subsystem grounds comparative claims, verifies capability evidence, and computes mathematical similarity percentages.

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/rag/loaders.py`
- **Purpose**: Unified multi-format document parser.
- **How It Works**:
  - Implements dedicated loaders for `PDF` (via `pypdf`), `DOCX` (via `python-docx`), plain text (`TXT`), and Markdown (`MD`).
  - Extracts clean, unformatted text while preserving structural document metadata such as source filenames, section headers, page numbers, and byte positions.
  - Validates files against `MAX_UPLOAD_MB` (default 15MB) and `ALLOWED_UPLOAD_TYPES` before memory extraction.

### 2. `backend/app/rag/chunking.py`
- **Purpose**: Semantic and structural text segmentation.
- **How It Works**:
  - Employs a recursive character and token splitting strategy with `CHUNK_SIZE=600` and `CHUNK_OVERLAP=100`.
  - Prioritizes semantic boundaries (double line breaks, markdown headers `#`, sentence periods) to avoid slicing technical tables or code parameters in half.
  - Every chunk receives a deterministic UUID, parent document reference, sequential index, and offset span.

### 3. `backend/app/rag/embeddings.py`
- **Purpose**: Dense semantic vector generation using Google's `EmbeddingGemma 2`.
- **How It Works**:
  - Loads `google/embeddinggemma-2` (`EMBEDDING_MODEL`) on the configured device (`EMBEDDING_DEVICE=cpu`).
  - Produces dense 768-dimensional embeddings (`EMBEDDING_DIM=768`) supporting sequences up to 8,192 tokens (`EMBEDDING_MAX_TOKENS=8192`).
  - Normalizes every embedding vector with L2 unit-norm ($||v||_2 = 1.0$), ensuring that Euclidean inner product operations equal exact cosine similarity.
  - *Note*: Asymmetric instruction formatting ("task: search result" / "query:") is applied per the model card specification.

### 4. `backend/app/rag/faiss_store.py`
- **Purpose**: Dense vector storage and similarity search.
- **How It Works**:
  - Uses FAISS `IndexFlatIP` (Inner Product). Because embeddings are normalized, inner product directly calculates cosine similarity with zero precision degradation.
  - Maintains a bidirectional ID map matching FAISS integer offsets to chunk UUIDs and document metadata stored in SQLite.
  - Persists index binary files under `FAISS_INDEX_DIR=./data/indexes`.

### 5. `backend/app/rag/bm25_index.py`
- **Purpose**: Lexical sparse inverted index for exact keyword matching.
- **How It Works**:
  - Builds an in-memory `Rank-BM25` (`BM25Okapi`) index over tokenized chunks.
  - While dense embeddings capture semantic synonyms, BM25 captures exact acronyms, model identifiers (e.g. `RTX-4090`), version numbers, and API flag names that dense models occasionally smooth over.
  - Serializes token dictionaries and inverted frequencies alongside the FAISS index.

### 6. `backend/app/rag/hybrid_retriever.py`
- **Purpose**: Fusion of dense and sparse retrieval ranks.
- **How It Works**:
  - Executes simultaneous concurrent search against the FAISS dense index and the BM25 sparse index.
  - Fuses rankings using Reciprocal Rank Fusion (RRF) and linear weighting governed by `HYBRID_DENSE_WEIGHT=0.6` ($Score = 0.6 	imes Dense + 0.4 	imes Sparse$).
  - Returns the top `RETRIEVE_TOP_K=8` candidate chunks for evaluation.

### 7. `backend/app/rag/reranker.py`
- **Purpose**: High-precision cross-encoder reranking.
- **How It Works**:
  - Controlled by `RERANKER_ENABLED=false` (toggleable in `.env`).
  - Uses `BAAI/bge-reranker-v2-m3` to score `(query, chunk_text)` pairs through full cross-attention, surfacing high-fidelity technical evidence.

### 8. `backend/app/rag/similarity.py`
- **Purpose**: Aggregating chunk similarity into 0-100% capability scores.
- **How It Works**:
  - Evaluates similarity scores using `SIMILARITY_AGGREGATION=topk_mean`.
  - Takes the arithmetic mean of top-k chunk similarities (`SIMILARITY_TOP_K=5`):
    $$	ext{Score} = rac{1}{K} \sum_{i=1}^K \cos(\mathbf{q}, \mathbf{c}_i)$$
  - Maps cosine values to a calibrated 0-100% capability alignment scale, providing explainable metrics in comparison matrices.

### 9. `backend/app/rag/grounding.py`
- **Purpose**: Evidence formatting and prompt injection.
- **How It Works**:
  - Formats retrieved chunks into standardized evidence snippets with explicit source citations (document name, page number, relevance score).
  - Supplies context to scoring and verdict nodes, enforcing that any factual claims cite concrete evidence.

### 10. `backend/app/agents/nodes/rag_ground.py`
- **Purpose**: Agentic retrieval grading and self-correction loop.
- **How It Works**:
  - Invokes LLM grader prompt `grader.md` to evaluate whether retrieved chunks provide sufficient factual evidence for the current criterion.
  - **Self-Correction Retry Loop**: If retrieved evidence is deemed irrelevant or insufficient:
    1. Grader identifies missing information.
    2. Query rewriter generates an expanded, reformulated query.
    3. Re-executes hybrid retrieval.
    4. Loop is strictly bounded by `MAX_REWRITE_LOOPS=2`.
  - If sufficient grounding cannot be found after 2 rewrites, the criterion is flagged as `Unverified in uploaded documentation`, preventing hallucinated claims.
