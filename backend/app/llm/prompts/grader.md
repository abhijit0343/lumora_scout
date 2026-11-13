# RAG Retrieval Grader Prompt Specification

## Purpose
Evaluates whether retrieved grounding snippets from uploaded reference documents provide sufficient, relevant, and verifiable factual evidence for target comparison criteria.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_DEFAULT=medium`
- Note: VERIFY ON MODEL CARD for binary classification prompting constraints.

## Input Variables
- `criterion`: Current comparison criterion being evaluated.
- `retrieved_snippets`: Retrieved document chunks from hybrid FAISS/BM25 search.

## Output Schema
JSON object:
- `is_relevant`: Boolean indicator (`true` or `false`).
- `confidence_score`: Float between 0.0 and 1.0.
- `missing_information`: Description of missing facts if relevance is inadequate.
- `suggested_query_rewrite`: Optimized search query to execute if retry loop is triggered.
