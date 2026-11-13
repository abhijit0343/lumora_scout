"""
Purpose: Hugging Face Hub tool extracting model card metadata, parameters, licenses, and benchmark scores.
Inputs: Hugging Face model repository ID (e.g., google/embeddinggemma-2).
Outputs: Model metadata dictionary (parameters, license, pipeline tag, readme content).
Dependencies: huggingface-hub, app.core.config. Note: VERIFY ON MODEL CARD for repo requirements.
TODOs:
  - Query Hugging Face Hub API using HF_TOKEN if configured.
  - Extract model card README and structured config metadata.
"""
