# Capability Extractor Prompt Specification

## Purpose
Analyzes scraped web pages, documentation, and API/tool metadata for a single target to extract structured capabilities, supported features, limitations, and direct evidentiary quotes.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_EXTRACT=medium`
- Note: VERIFY ON MODEL CARD for context length limits and multi-turn prompt templates.

## Input Variables
- `target_name`: Canonical name of the target product.
- `target_url`: Source URL of scraped content.
- `scraped_content`: Cleaned, sanitized page text filtered by L3 guardrails.
- `tool_metadata`: Supplementary metadata from stores, GitHub, or specialized tools.

## Output Schema
JSON array of capability records:
- `capability_id`: Unique identifier slug.
- `name`: Feature or capability name.
- `category`: Functional domain (e.g., Security, Pricing, API, Scalability).
- `status`: Supported (`yes`), Unsupported (`no`), Partial (`partial`), or Unknown (`unknown`).
- `details`: Detailed technical explanation.
- `evidence`: Direct excerpt or citation from source text.
