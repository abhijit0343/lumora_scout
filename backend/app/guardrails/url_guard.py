"""
Purpose: L2 URL guardrail canonicalizing schemes, following redirects safely, checking blocklists and Safe Browsing.
Inputs: Target URL string.
Outputs: Normalized safe URL or security rejection exception.
Dependencies: httpx, tldextract, app.core.config, app.guardrails.blocklists.loader.
TODOs:
  - Enforce strict http/https URL scheme and canonicalize domain names.
  - Follow redirects safely up to 5 hops using lightweight HEAD requests to inspect final destination.
  - Check domain against custom blocklists loaded from BLOCKLIST_DIR.
  - Query Google Safe Browsing API v4 with SAFE_BROWSING_API_KEY for malware and phishing reputation.
"""
