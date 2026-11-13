"""
Purpose: Comparative verdict node synthesizing executive analysis, trade-offs, and streamed recommendations.
Inputs: CompareState containing populated matrix, scores, and grounding snippets.
Outputs: State updates with synthesized verdict text and recommendation summary.
Dependencies: app.llm.gemini_client, app.llm.fallback_chain.
TODOs:
  - Invoke high-thinking LLM using verdict.md prompt to synthesize final comparative verdict.
  - Stream generated tokens to client via SSE token events.
  - Populate final verdict in state.
"""
