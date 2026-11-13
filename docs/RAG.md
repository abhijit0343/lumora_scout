# Retrieval-Augmented Generation (RAG) Architecture

## Metadata
- **Purpose**: Specifies the document ingestion pipeline, vector and lexical indexing architectures, hybrid retrieval, similarity scoring mathematics, and agentic self-correction loop for Lumora Scout.
- **Scope**: Covers document loaders, chunking strategies, EmbeddingGemma 2 embeddings, FAISS and BM25 store integration, reranking, similarity aggregation, and relevance grading loops.
- **Owner files**: `backend/app/rag/loaders.py`, `backend/app/rag/chunking.py`, `backend/app/rag/embeddings.py`, `backend/app/rag/faiss_store.py`, `backend/app/rag/bm25_index.py`, `backend/app/rag/hybrid_retriever.py`, `backend/app/rag/reranker.py`, `backend/app/rag/similarity.py`, `backend/app/rag/grounding.py`, `backend/app/agents/nodes/rag_ground.py`.

---

## 1. Document Ingestion Pipeline

### 1.1 Document Loading (`loaders.py`)
- Accepts file uploads via `POST /documents` constrained by `MAX_UPLOAD_MB=15` and `ALLOWED_UPLOAD_TYPES=pdf,docx,txt,md`.
- Extracts structured text and document metadata (source filename, page numbers, section headers) using dedicated format parsers.

### 1.2 Chunking Strategy (`chunking.py`)
- **Window Size**: 600 characters/tokens (`CHUNK_SIZE=600`).
- **Overlap**: 100 characters/tokens (`CHUNK_OVERLAP=100`).
- **Boundary Preservation**: Splits text respecting natural paragraph boundaries, sentence terminations, and markdown headers to maintain semantic coherence.
- Each chunk preserves metadata linking back to document ID, parent section, and byte offsets.

### 1.3 Dense Embeddings with EmbeddingGemma 2 (`embeddings.py`)
- Utilizes `google/embeddinggemma-2` (`EMBEDDING_MODEL`) producing dense 768-dimensional vectors (`EMBEDDING_DIM=768`).
- Operates on text modality (`EMBEDDING_MODALITIES=text`) executed on configured hardware (`EMBEDDING_DEVICE=cpu`).
- Input sequences are bounded by `EMBEDDING_MAX_TOKENS=8192`.
- Vectors undergo L2 unit-norm normalization prior to index storage.
- *NOTE*: VERIFY ON MODEL CARD for model loading procedures, asymmetric prefix prompts (e.g., query vs document prefixes), and dimension options.

### 1.4 Dual Storage Architecture (`faiss_store.py`, `bm25_index.py`)
- **Dense Store**: FAISS `IndexFlatIP` utilizing inner product over normalized vectors to compute exact cosine similarity without quantization loss. Indexes persist under `FAISS_INDEX_DIR=./data/indexes`.
- **Sparse Store**: Rank-BM25 inverted lexical index built over chunk tokens to capture exact technical specifications, model numbers, and rare keywords.
- **Metadata Persistence**: SQLite relational store mapping vector/BM25 ordinal indices to chunk content, document provenance, and timestamp.

---

## 2. Query & Retrieval Path

### 2.1 Hybrid Retrieval (`hybrid_retriever.py`)
- Given a query or capability requirement, computes normalized dense query embedding and tokenized query terms.
- Retrieves top candidates from FAISS (`IndexFlatIP`) and BM25 index.
- Fuses dense and sparse rankings using Reciprocal Rank Fusion (RRF) and linear score weighting controlled by `HYBRID_DENSE_WEIGHT=0.6` to retrieve candidate pool (`RETRIEVE_TOP_K=8`).

### 2.2 Optional Cross-Encoder Reranking (`reranker.py`)
- Controlled by `RERANKER_ENABLED=false` and `RERANKER_MODEL=BAAI/bge-reranker-v2-m3`.
- When enabled, passes (query, chunk_text) pairs through the cross-encoder to compute refined relevance scores, prioritizing high-fidelity technical evidence.

### 2.3 Grounding Snippets Extraction (`grounding.py`)
- Formats retrieved chunks into verifiable grounding snippets with source attribution, document name, and confidence indicators for LLM contextual injection.

---

## 3. Capability Similarity Scoring

### 3.1 Aggregation Mathematics (`similarity.py`)
- Aggregates chunk similarity scores into product/criterion scores using `SIMILARITY_AGGREGATION=topk_mean`.
- Takes the mean of top-k chunk similarities (`SIMILARITY_TOP_K=5`) for each evaluated capability dimension.
- Maps aggregated cosine values to a calibrated 0-100% capability alignment scale, providing explainable quantitative metrics in comparison matrices.

---

## 4. Agentic Self-Correction Loop

### 4.1 Retrieval Grading & Query Rewriting (`rag_ground.py`)
- Integrated within LangGraph node `rag_ground` using evaluation prompt `grader.md`.
- Evaluates whether retrieved grounding snippets provide sufficient, relevant evidence to score the target criteria.
- **Retry Condition**: If retrieved evidence is graded as insufficient or irrelevant:
  - Invokes LLM query reformulator to generate alternative keyword queries and semantic expansions.
  - Re-executes hybrid retrieval against indexed stores.
  - Loop is bounded by `MAX_REWRITE_LOOPS=2`.
- If maximum loops are exhausted without sufficient grounding, the system flags the criterion as unverified in user-facing matrices rather than hallucinating unsupported claims.
