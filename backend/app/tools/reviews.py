"""
Purpose: Aggregated user review tool summarizing sentiment and key feedback from public platforms.
Inputs: Product name or domain identifier.
Outputs: Aggregated review summary dictionary with sentiment scores and frequent pros/cons.
Dependencies: app.tools.web_search, app.llm.fallback_chain.
TODOs:
  - Search web for user review threads, Reddit discussions, and review aggregators.
  - Summarize sentiment patterns and repeated user criticisms.
"""
