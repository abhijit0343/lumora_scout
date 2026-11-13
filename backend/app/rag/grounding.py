"""
Purpose: Grounding snippet formatter extracting and attributing verifiable evidence for LLM prompt context.
Inputs: Retrieved and reranked chunks with document metadata.
Outputs: Formatted markdown grounding context with citations and document references.
Dependencies: app.schemas.capability.
TODOs:
  - Format chunk text excerpts with document names, page numbers, and relevance tags.
  - Construct grounding prompt context for injection into scoring and verdict nodes.
"""
