"""
Purpose: Similarity aggregation calculator mapping chunk similarities into 0-100% capability percentages.
Inputs: List of chunk similarity scores for a specific criterion.
Outputs: Calibrated capability percentage score (0 - 100%).
Dependencies: app.core.config.
TODOs:
  - Aggregate chunk scores using SIMILARITY_AGGREGATION=topk_mean over SIMILARITY_TOP_K=5 chunks.
  - Apply calibration curve mapping cosine similarity values to intuitive 0-100% metrics.
"""
