"""
Purpose: Pydantic request payload models for comparison initiation, checkpoint resumption, and cancellation.
Inputs: Incoming JSON request bodies from API clients.
Outputs: Validated CompareRequest, ResumeRequest, and CancelRequest models.
Dependencies: pydantic, typing.
TODOs:
  - Define CompareRequest schema (target_a, target_b, user_instructions, document_ids).
  - Define ResumeRequest schema (thread_id, checkpoint_type, action, modified_targets, modified_criteria).
"""
