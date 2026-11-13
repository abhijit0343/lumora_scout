"""
Purpose: Capability scoring node calculating quantitative metrics and similarity percentages across criteria.
Inputs: CompareState containing aligned matrix and RAG grounding context.
Outputs: State updates with computed scores, similarity percentages, and criterion evaluations.
Dependencies: app.rag.similarity, app.schemas.capability.
TODOs:
  - Compute quantitative scores for each criterion based on capability evidence and RAG context.
  - Calculate top-k chunk mean similarity percentages using SIMILARITY_AGGREGATION setting.
  - Update aligned matrix rows with definitive comparative evaluations.
"""
