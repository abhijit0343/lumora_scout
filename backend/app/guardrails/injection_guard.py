"""
Purpose: L1 prompt injection and jailbreak detector using heuristic signatures and fast classifier LLM.
Inputs: Raw user prompt text.
Outputs: Injection check result with boolean is_safe and confidence score.
Dependencies: app.llm.gemini_client, app.core.config.
TODOs:
  - Screen input text against known jailbreak patterns and delimiter hijacking tokens.
  - Invoke GUARD_CLASSIFIER_MODEL (gemini-3.8-flash) using guard_classifier.md prompt.
  - Flag adversarial prompt injections and system prompt leakage attempts.
"""
