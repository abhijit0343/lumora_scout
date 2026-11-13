"""
Purpose: Pydantic schemas for all Server-Sent Events (SSE) event types emitted by Lumora Scout.
Inputs: Graph state updates, tool logs, tokens, interrupts, guardrail violations.
Outputs: Structured SSE event models (StatusEvent, ToolStartEvent, InterruptEvent, MatrixRowEvent, TokenEvent, DoneEvent).
Dependencies: pydantic, typing.
TODOs:
  - Define base SSEEvent schema with thread_id, event_type, and timestamp.
  - Implement dedicated schemas for each of the 10 defined SSE event types.
"""
