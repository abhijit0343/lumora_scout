"""
Purpose: The Movie Database (TMDB) API tool for media, movie, and streaming comparison metadata.
Inputs: Movie or TV series title query string.
Outputs: Structured TMDB metadata record (genres, runtime, ratings, release date).
Dependencies: httpx, app.core.config.
TODOs:
  - Query TMDB API using TMDB_API_KEY.
  - Apply TMDB_INCLUDE_ADULT and MAX_CONTENT_CERTIFICATION filters to exclude adult content.
"""
