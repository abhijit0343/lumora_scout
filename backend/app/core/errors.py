"""
Purpose: Custom exception classes and global HTTP error handling handlers for Lumora Scout.
Inputs: Application exceptions, validation errors, guardrail violation events.
Outputs: JSON HTTP responses with standardized error envelopes.
Dependencies: fastapi, starlette.status.
TODOs:
  - Define LumoraBaseException, GuardrailViolationException, and CheckpointNotFoundException.
  - Implement exception handler translating domain errors into structured JSON responses.
"""
