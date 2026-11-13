"""
Purpose: FastAPI dependency injection providers for settings, checkpointer, and LLM clients.
Inputs: FastAPI request context and application state.
Outputs: Shared singleton or request-scoped instances of application services.
Dependencies: fastapi, app.core.config, app.persistence.checkpointer.
TODOs:
  - Provide get_settings dependency returning validated Settings.
  - Provide get_checkpointer dependency yielding active SQLite checkpointer.
"""
