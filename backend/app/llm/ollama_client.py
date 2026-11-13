"""
Purpose: Local Ollama client wrapper connecting to self-hosted qwen2.5:7b for offline local fallback.
Inputs: Prompt messages, system instructions, model tags.
Outputs: Generated text completions from local inference.
Dependencies: langchain-ollama, app.core.config. Note: VERIFY ON MODEL CARD for local hardware requirements.
TODOs:
  - Initialize ChatOllama client pointing to OLLAMA_BASE_URL.
  - Bind model to OLLAMA_MODEL (qwen2.5:7b).
  - Implement health check verifying Ollama daemon readiness.
"""
