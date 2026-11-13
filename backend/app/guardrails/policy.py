"""
Purpose: Master safety policy coordinator enforcing L1-L4 checks and managing uncertain-action workflows.
Inputs: User queries, URLs, scraped content, generated output text.
Outputs: GuardrailDecision object indicating pass, block, or ask (HITL interrupt).
Dependencies: app.core.config, app.guardrails.input_guard, app.guardrails.url_guard, app.guardrails.output_guard.
TODOs:
  - Coordinate evaluation pipeline across all 4 defense-in-depth layers.
  - Evaluate uncertain classification results against GUARD_UNCERTAIN_ACTION policy.
  - Emit audit log events for all safety evaluations.
"""
