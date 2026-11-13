"""
Purpose: System health check and diagnostic endpoint verifying model and store connectivity.
Inputs: HTTP GET request to /health.
Outputs: JSON object containing system status, model provider availability, and checkpointer state.
Dependencies: fastapi, app.core.config, app.llm.fallback_chain.
TODOs:
  - Check availability of primary LLM provider (Gemini) and fallbacks.
  - Verify read/write connectivity to SQLite checkpoints database.
  - Return 200 OK with detailed diagnostics payload.
"""
