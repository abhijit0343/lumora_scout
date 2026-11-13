"""
Purpose: Pydantic schemas for extracted capabilities, comparison criteria, and scored matrix rows.
Inputs: Extracted feature data, aligned criteria lists, and capability scores.
Outputs: Validated Capability, Criterion, and ComparisonMatrixRow models.
Dependencies: pydantic, typing.
TODOs:
  - Define Capability model (id, name, category, status, details, evidence).
  - Define Criterion model (id, name, importance, evaluation_guideline).
  - Define ComparisonMatrixRow model linking criterion to Side A and B evidence.
"""
