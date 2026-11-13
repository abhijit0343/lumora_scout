"""
Purpose: RAG grounding node retrieving uploaded document context and executing relevance grading retry loop.
Inputs: CompareState containing aligned criteria and document IDs.
Outputs: State updates containing retrieved grounding snippets, or trigger for query rewrite loop.
Dependencies: app.rag.hybrid_retriever, app.rag.reranker, app.rag.grounding, app.llm.fallback_chain.
TODOs:
  - Retrieve relevant chunks from FAISS and BM25 indexes for each comparison criterion.
  - Grade retrieval relevance using grader.md prompt.
  - If evidence is insufficient, execute rewrite loop up to MAX_REWRITE_LOOPS=2.
  - Attach grounding snippets and citations to state.
"""
