"""
Purpose: L1 input guardrail node validating input length, character safety, and detecting prompt injection.
Inputs: CompareState containing user_query and raw targets.
Outputs: State updates with guardrail_status and error_message if blocked.
Dependencies: app.guardrails.input_guard, app.guardrails.injection_guard.
TODOs:
  - Execute input_guard checks on query length and character set.
  - Execute injection_guard using fast classifier to detect adversarial prompt injections.
  - Route to terminal error state if check fails; otherwise proceed to resolve.
"""
