# Entity Resolver Prompt Specification

## Purpose
Resolves ambiguous user references into canonical entity names, primary homepages, documentation URLs, and catalog definitions for Side A and Side B.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_ROUTER=low`
- Note: VERIFY ON MODEL CARD for tool-calling syntax and structured schema support.

## Input Variables
- `target_a_raw`: Raw string or URL for side A.
- `target_b_raw`: Raw string or URL for side B.
- `search_context`: Supplementary search snippets from Tavily/Brave search tools.

## Output Schema
JSON object containing structured `CatalogItem` records for both targets:
- `name`: Canonical product / site name.
- `url`: Official homepage or target landing URL.
- `domain`: Fully-qualified domain name.
- `entity_type`: Category classification.
- `summary`: One-sentence entity description.
