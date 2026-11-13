"""
Purpose: Utility for enforcing Pydantic structured output extraction across diverse LLM providers.
Inputs: LLM client instance, prompt message, target Pydantic model class.
Outputs: Instantiated and validated Pydantic model object.
Dependencies: pydantic, langchain-core.
TODOs:
  - Implement with_structured_output wrapper supporting native tool calling and JSON mode.
  - Implement schema repair fallback when JSON parsing encounters minor syntax errors.
"""
