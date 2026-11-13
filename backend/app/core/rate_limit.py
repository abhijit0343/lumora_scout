"""
Purpose: Client IP rate limiting provider using SlowAPI to prevent abuse and denial-of-service.
Inputs: Incoming FastAPI Request objects containing client host addresses.
Outputs: Limiter decorator and dependency instances enforcing request thresholds.
Dependencies: slowapi, slowapi.util, app.core.config.
TODOs:
  - Initialize SlowAPI Limiter using get_remote_address key function.
  - Apply RATE_LIMIT_PER_MIN limit default across public compare endpoints.
"""
