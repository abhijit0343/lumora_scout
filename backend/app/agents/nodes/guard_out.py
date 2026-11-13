"""
Purpose: L4 output guardrail node scanning synthesized verdict and matrix before emitting terminal done event.
Inputs: CompareState containing final verdict and comparison matrix.
Outputs: Verified final state or sanitized output free from leaks or toxic text.
Dependencies: app.guardrails.output_guard.
TODOs:
  - Scan output stream and verdict for accidental system prompt leakage or internal secrets.
  - Redact any sensitive PII detected in output.
  - Emit terminal done SSE event.
"""
