"""
Purpose: Comparison API route handlers for initiating streams, resuming HITL checkpoints, and state queries.
Inputs: HTTP requests to /compare/stream, /compare/resume, /compare/{thread}/state, /compare/{thread}/cancel.
Outputs: EventSource SSE streams and JSON session snapshot objects.
Dependencies: fastapi, sse-starlette, app.schemas.requests, app.agents.graph, app.api.sse.
TODOs:
  - Implement POST /compare/stream endpoint kicking off LangGraph and streaming SSE events.
  - Implement POST /compare/resume endpoint resuming graph from Checkpoint A, B, or C.
  - Implement GET /compare/{thread}/state fetching current session snapshot.
  - Implement POST /compare/{thread}/cancel terminating running background task.
"""
