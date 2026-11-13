# 4-Layer Safety Guardrails Specification

## Metadata
- **Purpose**: Defines the comprehensive 4-layer defensive safety architecture protecting Lumora Scout against malicious user inputs, malicious destination sites, unsafe scraped payloads, and unsafe generated verdicts.
- **Scope**: Covers L1 Input Guardrails, L2 URL/SSRF Guardrails, L3 Content Ingestion Guardrails, L4 Output Guardrails, uncertain-result handling, security logging, defensive limits, and red-team evaluation plans.
- **Owner files**: `backend/app/guardrails/policy.py`, `backend/app/guardrails/input_guard.py`, `backend/app/guardrails/injection_guard.py`, `backend/app/guardrails/url_guard.py`, `backend/app/guardrails/ssrf_guard.py`, `backend/app/guardrails/content_guard.py`, `backend/app/guardrails/output_guard.py`, `backend/app/guardrails/blocklists/loader.py`, `backend/app/agents/nodes/guard_in.py`, `backend/app/agents/nodes/guard_urls.py`, `backend/app/agents/nodes/guard_out.py`.

---

## 1. Layer 1: Input Guardrails (Pre-Execution)
The L1 guardrail runs immediately upon receiving user input before any tool invocation or entity resolution begins.

### L1.1 Input Structural & Policy Guard (`input_guard.py`)
- **Length & Payload Boundaries**: Enforces strict character and token limits on comparison inputs (target names and query parameters) to prevent resource exhaustion attacks.
- **Disallowed Character Sets**: Sanitizes non-printable characters, bidirectional override Unicode exploits, and malformed encoding sequences.
- **Domain Policy Enforcement**: Rejects queries requesting evaluations of forbidden categories such as illegal goods, explicit adult material, malicious software, or weapons.

### L1.2 Prompt Injection & Jailbreak Guard (`injection_guard.py`)
- **Heuristic Pattern Matching**: Screens input text for delimiter hijacking tokens, known jailbreak signatures (such as "DAN", role-reversal imperatives, and instruction-negation tokens).
- **Fast Model Classification**: Invokes `GUARD_CLASSIFIER_MODEL` (`gemini-3.8-flash` with low thinking level) using `guard_classifier.md` to classify adversarial intent, system prompt leakage attacks, and indirect instruction overrides.

---

## 2. Layer 2: URL & SSRF Guardrails (Pre-Fetch)
The L2 guardrail validates and hardens all resolved or user-supplied URLs before any network requests are dispatched.

### L2.1 URL Reputation & Normalization Guard (`url_guard.py`)
- **Canonicalization & Scheme Enforcement**: Restricts protocols strictly to `http` and `https`. Normalizes punycode, URL-encoded characters, and port designations.
- **Redirect Resolution**: Follows redirects safely up to a strict limit of 5 hops using lightweight HEAD requests to inspect the terminal destination URL prior to scraping.
- **Blocklist Filtering**: Intersects target domains against compiled domain blocklists loaded via `loader.py` from `BLOCKLIST_DIR`.
- **Google Safe Browsing API**: Queries Google Safe Browsing v4 endpoints with `SAFE_BROWSING_API_KEY` to verify that destination hosts are not flagged for malware, social engineering, or unwanted software.
- **Re-check on Edited URLs**: When a human operator modifies or substitutes target URLs during Human-in-the-Loop Checkpoint A, the modified URLs must pass L2 validation in full before resumption.

### L2.2 SSRF Protection (`ssrf_guard.py`)
- **DNS Resolution & IP Inspection**: Resolves destination hostnames to target IPv4 and IPv6 addresses prior to socket connection.
- **Private & Reserved Range Blacklisting**: If `SSRF_BLOCK_PRIVATE_RANGES=true`, blocks resolution to loopback (`127.0.0.0/8`, `::1`), RFC 1918 private spaces (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), link-local spaces (`169.254.0.0/16`, `fe80::/10`), carrier-grade NAT, and cloud metadata instances (`169.254.169.254`).
- **DNS Rebinding Defense**: Pinning resolved IP addresses for subsequent HTTP extraction requests to prevent time-of-check to time-of-use (TOCTOU) DNS rebinding attacks.

---

## 3. Layer 3: Scraped Content Guardrails (Post-Fetch, Pre-Reasoning)
The L3 guardrail filters untrusted scraped content before raw web text reaches the primary LLM context window.

### L3.1 Ingestion Content Screening (`content_guard.py`)
- **Size and Bandwidth Limiting**: Enforces strict cutoffs at `MAX_PAGE_BYTES` (2 MB) and timeout at `FETCH_TIMEOUT_S` (15s) to guard against compression bombs and slow-loris scraper traps.
- **Harmful Content Filtering**: Scans extracted HTML/text using classifier checks to detect illicit content, hate speech, adult content violating `MAX_CONTENT_CERTIFICATION`, and malicious script injection.
- **Indirect Prompt Injection Neutralization**: Strips prompt injection traps embedded inside hidden HTML tags, zero-font text, metadata attributes, or markdown comments designed to hijack comparative reasoning.

---

## 4. Layer 4: Output Guardrails (Post-Synthesis)
The L4 guardrail inspects synthesized analysis, capability matrices, and final comparison verdicts before streaming to the client.

### L4.1 Verdict Integrity & Leakage Guard (`output_guard.py`)
- **System Prompt & Secret Scrubbing**: Scans output streams for accidental exposure of internal system prompts, API keys, internal network endpoints, or raw environment variables.
- **PII Redaction**: Redacts accidentally extracted personal identifying information (PII) including email addresses, phone numbers, and authentication tokens.
- **Defamation & Safety Re-verification**: Validates that comparative claims remain professional, grounded in retrieved source artifacts, and free from abusive or unverified harmful allegations.

---

## 5. Operational Policies & Auditing

### 5.1 Uncertain-Result Policy
- Configured by `GUARD_UNCERTAIN_ACTION` (`ask` vs `block`).
- When a classifier returns a confidence score falling inside the ambiguous safety band (between 0.35 and 0.70):
  - If set to `ask`: Pauses graph execution at HITL Checkpoint C, streaming a guarded interrupt event with the flagged concern to allow explicit human operator sign-off.
  - If set to `block`: Immediately aborts processing, logs a security event, and emits an SSE `blocked` event with an informative refusal message.

### 5.2 Security Logging & Audit Trails
- All guardrail evaluations emit structured JSON log entries recording thread ID, timestamp, layer ID, decision status, target domain hash, and flagged violation category.
- Raw sensitive payloads and PII are never persisted to long-term storage or application logs.

### 5.3 Red-Team Testing Strategy
- The test suite in `backend/tests/guardrails_redteam/` executes automated adversarial evaluations including:
  - Direct prompt injection variants and token smuggling techniques.
  - SSRF evasion vectors including IPv6 equivalents, decimal/hex IP encodings, and DNS rebinding simulations.
  - Scraped content poisoning scenarios containing adversarial extraction traps.
  - Multi-hop redirect chains leading into restricted internal infrastructure.
