"""
Purpose: FastAPI application entrypoint configuring CORS, exception handlers, rate limiting, and routing.
Inputs: HTTP requests, startup lifecycle events, environment settings.
Outputs: FastAPI application instance exposing REST and SSE streaming endpoints.
Dependencies: fastapi, slowapi, uvicorn, app.core.config, app.api.routes.
TODOs:
  - Initialize FastAPI app with title and metadata from app.core.config.
  - Configure CORS middleware using allowed origins.
  - Attach SlowAPI rate limiter state and error handlers.
  - Include API routers for compare, documents, and health routes.
"""
