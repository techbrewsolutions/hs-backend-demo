import base64
import hmac
import hashlib
import time
from typing import Protocol

from src.domain.constants import URL_DECODE_MAP


class IRequestVerifier(Protocol):
    """Interface for request verification."""

    async def verify_request(
        self, method: str, url: str, body: str, timestamp: str, signature: str
    ) -> bool:
        """Verify a request using the provided parameters."""
        ...


class HubSpotRequestVerifier(IRequestVerifier):
    """Service for verifying HubSpot requests."""

    def __init__(self, client_secret: str):
        self.client_secret = client_secret

    async def verify_request(
        self, method: str, url: str, body: str, timestamp: str, signature: str
    ) -> bool:
        """
        Verify the request using the client secret for v3 signature.
        """
        if not timestamp:
            return False

        # Validate timestamp is not older than 5 minutes
        current_time = int(time.time() * 1000)
        timestamp_int = int(timestamp)
        if current_time - timestamp_int > 300000:  # 5 minutes in milliseconds
            return False

        # Decode URL-encoded characters
        request_uri = url
        for encoded, decoded in URL_DECODE_MAP.items():
            request_uri = request_uri.replace(encoded, decoded)

        # Create the string to hash
        raw_string = f"{method}{request_uri}{body}{timestamp}"

        # Create HMAC SHA-256 hash and base64 encode it
        computed_signature = hmac.new(
            self.client_secret.encode(), raw_string.encode(), hashlib.sha256
        ).digest()
        computed_signature = base64.b64encode(computed_signature).decode()

        # Compare signatures (using constant-time comparison)
        return hmac.compare_digest(computed_signature, signature)
