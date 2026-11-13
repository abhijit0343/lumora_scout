"""
Purpose: Pydantic schemas for canonical comparison target entities, products, and websites.
Inputs: Raw entity strings or resolved URL metadata.
Outputs: Validated CatalogItem data structures with canonical names, URLs, domains, and entity types.
Dependencies: pydantic.
TODOs:
  - Define CatalogItem schema with name, url, domain, entity_type, summary, and metadata.
  - Add validators ensuring valid HTTP/HTTPS schemes and normalized domains.
"""
