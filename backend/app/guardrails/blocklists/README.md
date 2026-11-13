# Custom Guardrail Blocklists

## Purpose
Houses curated lists of restricted domains, malicious hosts, phishing URLs, and prohibited competitive targets.

## Directory Structure
- `domains.txt`: Prohibited top-level domains and fully qualified domain names (one per line).
- `ip_ranges.txt`: Prohibited IP ranges and CIDR blocks for internal network protection.
- `keywords.txt`: High-risk keywords triggering enhanced classification.

## Loading Mechanism
Blocklists are parsed and indexed into in-memory hash sets by `backend/app/guardrails/blocklists/loader.py` during backend startup.

## Formatting Guidelines
- Lines starting with `#` are treated as comments.
- Blank lines are ignored.
- Supports wildcard domains (e.g., `*.malicious.example`).
