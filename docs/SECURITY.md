# Security Architecture & Threat Model

## Metadata
- **Purpose**: Defines threat models, security controls, vulnerability mitigations, and compliance postures.
- **Scope**: SSRF prevention, prompt injection mitigation, network isolation, credential safety, and data retention.
- **Owner files**: `backend/app/guardrails/*`, `backend/app/core/config.py`.

---

## 1. Threat Modeling Outline
- **Adversarial Prompt Injections**: Direct jailbreaks and indirect prompt injections embedded in target website DOM structures.
- **Server-Side Request Forgery (SSRF)**: Attempts to abuse scrapers to query internal network services, cloud metadata endpoints, or localhost services.
- **Denial of Service (DoS)**: High-frequency requests, recursive redirects, and compression bombs ("zip bombs" or gigabyte-scale HTML documents).
- **Data Exfiltration**: Malicious outputs designed to trick LLMs into disclosing system prompts, API keys, or uploaded document content.

## 2. Defensive Controls Outline
- **SSRF Hardening**: Pre-flight DNS resolution, private IP blacklisting (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.169.254`), and DNS pinning.
- **Rate Limiting**: IP-based rate limiting via SlowAPI (`RATE_LIMIT_PER_MIN=30`).
- **Resource Constraints**: Maximum upload limits (`MAX_UPLOAD_MB=15`), maximum page fetch sizes (`MAX_PAGE_BYTES=2000000`), and fetch timeouts (`FETCH_TIMEOUT_S=15`).
- **Credential Hygiene**: Zero secret hardcoding, strict `.env.example` placeholders, and automated scanning via git hooks.
