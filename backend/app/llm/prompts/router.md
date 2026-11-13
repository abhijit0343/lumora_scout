# Router Prompt Specification

## Purpose
Directs incoming comparison queries to the appropriate entity resolution strategy and identifies target domains, product categories, or specialized tools needed.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`) or fallback
- Thinking Level: `LLM_THINKING_LEVEL_ROUTER=low`
- Note: VERIFY ON MODEL CARD for model-specific system tags and schema formatting.

## Input Variables
- `user_query`: Raw user prompt describing the requested comparison.

## Output Schema
JSON object specifying:
- `category`: Product / service / platform category (e.g., `saas`, `mobile_app`, `github_repo`, `model_weights`, `media`).
- `intent`: Comparative analysis focus (e.g., `pricing`, `performance`, `developer_experience`, `features`).
- `requires_tools`: List of specific tools recommended for discovery.
