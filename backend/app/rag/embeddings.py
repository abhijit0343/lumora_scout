"""
Purpose: Dense vector embedding generator utilizing EmbeddingGemma 2 producing normalized 768-dim vectors.
Inputs: List of text chunks or search query strings.
Outputs: Normalized 768-dimensional NumPy float32 embedding arrays.
Dependencies: sentence-transformers, transformers, torch, app.core.config. Note: VERIFY ON MODEL CARD for prompt templates.
TODOs:
  - Load EmbeddingGemma 2 model from EMBEDDING_MODEL on configured EMBEDDING_DEVICE.
  - Apply L2 unit-norm normalization to output vectors.
  - Support asymmetric query and document prompt formatting per model card guidelines.
"""
