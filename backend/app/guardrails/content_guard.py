"""
Purpose: L3 scraped content guardrail screening fetched text for adult material, malware, and indirect prompt injection.
Inputs: Scraped HTML or raw text content.
Outputs: Sanitized clean text or content rejection exception.
Dependencies: app.core.config, app.llm.gemini_client.
TODOs:
  - Enforce MAX_PAGE_BYTES (2MB) limit and strip executable scripts.
  - Screen extracted content for indirect prompt injections hidden in comments, metadata, or zero-font text.
  - Classify content against MAX_CONTENT_CERTIFICATION and safety policies.
"""
