"""
Purpose: L2 URL guardrail node checking target URLs against redirects, blocklists, Safe Browsing, and SSRF filters.
Inputs: CompareState containing resolved or human-edited target URLs.
Outputs: State updates confirming URL safety or recording security rejection.
Dependencies: app.guardrails.url_guard, app.guardrails.ssrf_guard.
TODOs:
  - Validate target URLs with url_guard (canonicalization, redirect following, Safe Browsing API).
  - Inspect resolved destination IP addresses with ssrf_guard to block private/internal ranges.
  - Re-verify edited URLs if modified during Checkpoint A.
"""
