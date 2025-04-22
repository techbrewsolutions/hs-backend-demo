from typing import Callable

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from src.domain.services.verification import HubSpotRequestVerifier
from src.infrastructure.config import get_settings

settings = get_settings()


class HubSpotVerificationMiddleware(BaseHTTPMiddleware):
    """Middleware to verify HubSpot requests for contact routes."""

    def __init__(self, app):
        super().__init__(app)
        self.verifier = HubSpotRequestVerifier(settings.HUBSPOT_CLIENT_SECRET)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        # Only verify requests for contact routes
        if not request.url.path.startswith("/contacts"):
            return await call_next(request)

        # Get required headers
        timestamp = request.headers.get("X-HubSpot-Request-Timestamp")
        signature = request.headers.get("X-HubSpot-Signature-v3")

        # Get request body
        body = await request.body()
        body_str = body.decode("utf-8")

        # Verify the request
        is_valid = await self.verifier.verify_request(
            method=request.method,
            url=str(request.url),
            body=body_str,
            timestamp=timestamp,
            signature=signature,
        )

        if not is_valid:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid request"},
            )

        return await call_next(request)
