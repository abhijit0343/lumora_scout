"""
Purpose: Fast static web page scraper using HTTPX and Trafilatura to extract clean reader-mode text.
Inputs: Target URL string.
Outputs: Cleaned extracted text content and document metadata.
Dependencies: httpx, trafilatura, app.core.config.
TODOs:
  - Fetch static HTML using HTTPX with custom browser User-Agent and FETCH_TIMEOUT_S timeout.
  - Extract clean text and structural markdown using Trafilatura.
  - Enforce MAX_PAGE_BYTES payload size limit.
"""
