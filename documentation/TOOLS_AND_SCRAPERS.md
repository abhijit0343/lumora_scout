# External Tools & Web Scrapers

## Overview
Lumora Scout incorporates specialized tools to discover, retrieve, and parse technical specifications across websites, documentation portals, app stores, source repositories, and multimedia catalogs.

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/tools/web_search.py`
- **Purpose**: Autonomous web discovery and search.
- **How It Works**:
  - Connects to Tavily AI Search API (`TAVILY_API_KEY`) for clean, structured web content.
  - Automatically falls back to Brave Search API (`BRAVE_API_KEY`) if Tavily quota is exhausted.
  - Caches query responses in `cache.py` for `SEARCH_CACHE_TTL_S` (24 hours) to minimize API consumption.

### 2. `backend/app/tools/fetch_page.py`
- **Purpose**: Primary high-speed static page scraper.
- **How It Works**:
  - Uses `HTTPX` asynchronous client with browser User-Agent headers and a `FETCH_TIMEOUT_S=15` timeout.
  - Employs `trafilatura` to strip boilerplate (navigation bars, footers, cookie banners) and extract clean reader-mode text and markdown.
  - Enforces `MAX_PAGE_BYTES=2000000` (2MB limit).

### 3. `backend/app/tools/playwright_fetch.py`
- **Purpose**: Headless browser scraper for dynamic single-page applications.
- **How It Works**:
  - Triggered as a fallback when static scraping via `fetch_page.py` yields empty content or bot challenge screens (if `ALLOW_PLAYWRIGHT_FALLBACK=true`).
  - Launches headless Chromium via `playwright`, waits for network idle or selector rendering, and extracts client-rendered DOM content.

### 4. `backend/app/tools/app_store.py`
- **Purpose**: Apple iOS App Store capability and rating extractor.
- **How It Works**:
  - Parses iOS app store URLs or bundles.
  - Queries Apple iTunes Search API to retrieve structured metadata: version history, supported iOS versions, user ratings, and pricing tiers.

### 5. `backend/app/tools/play_store.py`
- **Purpose**: Google Play Store Android app extractor.
- **How It Works**:
  - Extracts package names from Google Play URLs.
  - Leverages `google-play-scraper` to pull install counts, content ratings, release notes, and developer specifications.

### 6. `backend/app/tools/hf_hub.py`
- **Purpose**: Hugging Face Hub machine learning model inspector.
- **How It Works**:
  - Interacts with Hugging Face Hub API using `HF_TOKEN`.
  - Extracts model card READMEs, tensor parameter counts, architecture tags, and open-source licenses for AI model comparisons.

### 7. `backend/app/tools/github.py`
- **Purpose**: Open-source repository metric extractor.
- **How It Works**:
  - Interacts with GitHub REST API using `GITHUB_TOKEN`.
  - Extracts stars, forks, recent commit velocity, issue closure rates, repository topics, and primary languages.

### 8. `backend/app/tools/tmdb.py`
- **Purpose**: Entertainment and media comparison tool.
- **How It Works**:
  - Queries The Movie Database (TMDB) API using `TMDB_API_KEY`.
  - Enforces `TMDB_INCLUDE_ADULT=false` and `MAX_CONTENT_CERTIFICATION=PG-13` to prevent adult media ingestion.

### 9. `backend/app/tools/reviews.py`
- **Purpose**: Public sentiment and user review aggregator.
- **How It Works**:
  - Synthesizes user reviews across Reddit discussions and public review aggregators.
  - Extracts common pain points, repeated user praise, and real-world stability feedback.
