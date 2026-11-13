"""
Purpose: Human-in-the-loop Checkpoint B node allowing operator review and adjustment of comparison criteria.
Inputs: CompareState containing aligned criteria list.
Outputs: Interrupt signal if criteria review is active, or transparent pass-through.
Dependencies: langgraph.types, app.core.config.
TODOs:
  - Check Settings.HITL_CONFIRM_CRITERIA setting.
  - If enabled, raise interrupt presenting criteria for operator re-ordering, additions, or pruning.
  - Upon resume, apply updated criteria to aligned_matrix in state.
"""
