"""
Purpose: L4 output safety guard verifying synthesized verdicts and matrix rows for PII, leaks, and safety.
Inputs: Generated verdict markdown text and comparison matrix.
Outputs: Sanitized output safe for client transmission.
Dependencies: app.core.config.
TODOs:
  - Scan output text for internal system prompt disclosures or leaked API keys.
  - Redact detected personal identifying information (PII) including emails and tokens.
  - Verify comparative claims maintain objective, grounded tone without abusive content.
"""
