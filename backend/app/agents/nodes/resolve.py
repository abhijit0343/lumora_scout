"""
Purpose: Entity resolution node resolving user inputs into canonical entities, URLs, and catalog items.
Inputs: CompareState containing raw targets A and B.
Outputs: State updates containing resolved CatalogItem records for target_a and target_b.
Dependencies: app.llm.fallback_chain, app.tools.web_search, app.schemas.catalog_item.
TODOs:
  - Search web for target names using Tavily/Brave tools if raw input is not a direct URL.
  - Invoke LLM with resolver.md prompt to identify canonical product names and homepages.
  - Populate resolved_target_a and resolved_target_b in state.
"""
