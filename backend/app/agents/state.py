"""
Purpose: LangGraph StateGraph state definition representing complete comparative session context.
Inputs: Graph node outputs and state update dictionaries.
Outputs: TypedDict CompareState instance tracked across graph nodes and SQLite checkpoints.
Dependencies: typing, typing_extensions, app.schemas.catalog_item, app.schemas.capability.
TODOs:
  - Define CompareState TypedDict with fields: thread_id, user_query, target_a_raw, target_b_raw.
  - Add fields for resolved targets, criteria, capabilities_a, capabilities_b, aligned_matrix.
  - Add fields for rag_grounding_context, scores, verdict, guardrail_status, interrupt_data, error_message.
"""
