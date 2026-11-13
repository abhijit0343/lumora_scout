# Persistence Layer & Caching

## Overview
Lumora Scout ensures complete state recovery across network disconnections and server restarts through relational storage and persistent checkpointers.

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/persistence/checkpointer.py`
- **Purpose**: SQLite-backed LangGraph state checkpointer.
- **How It Works**:
  - Initializes `SqliteSaver` connecting to `CHECKPOINT_DB_PATH=./data/checkpoints.sqlite`.
  - Enables Write-Ahead Logging (`PRAGMA journal_mode=WAL`) for concurrent read/write transactions.
  - Automatically commits serialized state snapshots after every graph node. When an operator resumes from an interrupt, the checkpointer restores state with 100% fidelity.

### 2. `backend/app/persistence/db.py`
- **Purpose**: Document catalog and comparison history store.
- **How It Works**:
  - Manages SQLite tables for uploaded documents, chunk metadata, and archived comparison reports.
  - Provides thread-safe session context managers.

### 3. `backend/app/persistence/cache.py`
- **Purpose**: Cache manager for web search and page scrapers.
- **How It Works**:
  - Caches Tavily/Brave search results and Trafilatura page markdown using SHA-256 URL hashes.
  - Enforces `SEARCH_CACHE_TTL_S=86400` (24-hour TTL) to prevent repeated web queries for unchanged target homepages.
