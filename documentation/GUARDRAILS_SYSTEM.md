# 4-Layer Defense-in-Depth Safety Guardrails

## Overview
Lumora Scout enforces four distinct layers of defensive guardrails. The system prevents direct and indirect prompt injections, protects infrastructure against Server-Side Request Forgery (SSRF), screens untrusted scraped web content before it reaches reasoning models, and scrubs sensitive information from final outputs.

---

## 🛡️ Guardrail Architecture Layers

```
Layer 1: Input Guardrails       ──► Checks user prompts & injection attempts before execution
Layer 2: URL & SSRF Guardrails  ──► Validates domains, redirects, IPs & Safe Browsing before fetch
Layer 3: Content Guardrails     ──► Screens scraped HTML/text before LLM context injection
Layer 4: Output Guardrails      ──► Scrubs PII, leaks, and toxicity before streaming to client
```

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/guardrails/policy.py`
- **Purpose**: Central policy coordinator and decision engine.
- **How It Works**:
  - Coordinates checks across L1, L2, L3, and L4.
  - Manages the **Uncertain-Result Policy** (`GUARD_UNCERTAIN_ACTION`):
    - When classifier confidence falls into the ambiguous band (0.35 to 0.70):
      - If set to `ask`: Pauses graph execution at HITL Checkpoint C, streaming an interrupt event to allow explicit human operator review.
      - If set to `block`: Immediately aborts processing and emits an SSE `blocked` event with an audit explanation.

### 2. `backend/app/guardrails/input_guard.py` (Layer 1)
- **Purpose**: Syntactic and structural validation of incoming user prompts.
- **How It Works**:
  - Enforces character length and token limits on comparison inputs to prevent buffer and memory exhaustion.
  - Sanitizes non-printable characters, zero-width characters, and bidirectional Unicode override exploits (`U+202E`).
  - Rejects queries evaluating prohibited topics (illicit goods, malware development, explicit adult material, weapons).

### 3. `backend/app/guardrails/injection_guard.py` (Layer 1)
- **Purpose**: Adversarial prompt injection and jailbreak detection.
- **How It Works**:
  - Evaluates prompts using heuristic signature scanning for known jailbreak tokens (e.g., "DAN", role-reversal imperatives, instruction delimiters `---`, `<|im_start|>`).
  - Dispatches `GUARD_CLASSIFIER_MODEL` (`gemini-3.8-flash` with low thinking level) using `guard_classifier.md` to classify adversarial intent, system prompt extraction, and instruction negation.

### 4. `backend/app/guardrails/url_guard.py` (Layer 2)
- **Purpose**: Target URL reputation, normalization, and redirect inspection.
- **How It Works**:
  - Restricts URL protocols strictly to `http` and `https`. Normalizes punycode, URL-encoded entities, and port values.
  - Follows HTTP redirects up to 5 hops using lightweight `HEAD` requests to verify the terminal destination URL prior to scraping.
  - Checks target domains against local blocklists loaded from `BLOCKLIST_DIR`.
  - Queries Google Safe Browsing API v4 using `SAFE_BROWSING_API_KEY` to ensure the host is not flagged for malware, phishing, or unwanted software.
  - Re-evaluates URLs if an operator manually edits them during HITL Checkpoint A.

### 5. `backend/app/guardrails/ssrf_guard.py` (Layer 2)
- **Purpose**: Server-Side Request Forgery (SSRF) defense.
- **How It Works**:
  - Resolves hostnames to underlying IPv4 and IPv6 addresses prior to socket connection.
  - When `SSRF_BLOCK_PRIVATE_RANGES=true`, blocks resolution to:
    - Loopback addresses (`127.0.0.0/8`, `::1`)
    - RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
    - Link-local and cloud metadata addresses (`169.254.169.254`, `fe80::/10`)
  - Employs DNS pinning to prevent Time-of-Check to Time-of-Use (TOCTOU) DNS rebinding attacks where a domain resolves to a safe IP during check, then resolves to an internal IP during fetch.

### 6. `backend/app/guardrails/content_guard.py` (Layer 3)
- **Purpose**: Scraped web page inspection before LLM context injection.
- **How It Works**:
  - Enforces payload bounds: cuts off streams at `MAX_PAGE_BYTES` (2MB) and times out at `FETCH_TIMEOUT_S` (15s) to mitigate decompression bombs.
  - Strips HTML tags, inline scripts, styles, and comments.
  - Detects **Indirect Prompt Injections**: screens hidden text, CSS `display:none` spans, zero-font text, and image `alt` attributes designed to hijack comparative reasoning when the page is read by an LLM.

### 7. `backend/app/guardrails/output_guard.py` (Layer 4)
- **Purpose**: Post-synthesis output verification and data loss prevention.
- **How It Works**:
  - Scans final verdict text and matrix rows for accidental exposure of system prompts, internal IP addresses, or API credentials.
  - Redacts Personal Identifiable Information (PII) including email addresses, phone numbers, and session tokens.
  - Verifies that comparative claims maintain an objective, professional tone without defamatory or ungrounded accusations.

### 8. `backend/app/guardrails/blocklists/loader.py` & `README.md`
- **Purpose**: High-speed in-memory custom blocklist repository.
- **How It Works**:
  - Parses `domains.txt`, `ip_ranges.txt`, and `keywords.txt` from `BLOCKLIST_DIR`.
  - Supports wildcard domain patterns (e.g., `*.malicious.org`) and CIDR network blocks.
  - Provides thread-safe $O(1)$ set lookups during Layer 2 evaluation.
