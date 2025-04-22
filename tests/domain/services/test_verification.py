import pytest
from unittest.mock import Mock, patch
import time
import hmac
import hashlib
import base64

from src.domain.services.verification import HubSpotRequestVerifier


@pytest.fixture
def verifier():
    """Create a HubSpotRequestVerifier instance for testing."""
    return HubSpotRequestVerifier(client_secret="test_secret")


@pytest.mark.asyncio
async def test_verify_request_missing_timestamp(verifier):
    """Test verification fails when timestamp is missing."""
    result = await verifier.verify_request(
        method="GET",
        url="https://example.com",
        body="",
        timestamp="",
        signature="test_signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_expired_timestamp(verifier):
    """Test verification fails when timestamp is expired."""
    # Create a timestamp 6 minutes ago (more than 5 minutes allowed)
    expired_timestamp = str(int((time.time() - 360) * 1000))  # 360 seconds = 6 minutes

    result = await verifier.verify_request(
        method="GET",
        url="https://example.com",
        body="",
        timestamp=expired_timestamp,
        signature="test_signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_valid_signature(verifier):
    """Test verification succeeds with valid signature."""
    # Create a valid timestamp (current time)
    current_timestamp = str(int(time.time() * 1000))

    # Create a test request
    method = "GET"
    url = "https://example.com"
    body = '{"test": "data"}'

    # Calculate expected signature
    raw_string = f"{method}{url}{body}{current_timestamp}"
    expected_signature = hmac.new(
        "test_secret".encode(), raw_string.encode(), hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(expected_signature).decode()

    result = await verifier.verify_request(
        method=method,
        url=url,
        body=body,
        timestamp=current_timestamp,
        signature=expected_signature,
    )
    assert result is True


@pytest.mark.asyncio
async def test_verify_request_invalid_signature(verifier):
    """Test verification fails with invalid signature."""
    current_timestamp = str(int(time.time() * 1000))

    result = await verifier.verify_request(
        method="GET",
        url="https://example.com",
        body="",
        timestamp=current_timestamp,
        signature="invalid_signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_url_decoding(verifier):
    """Test URL decoding works correctly."""
    current_timestamp = str(int(time.time() * 1000))

    # Test URL with encoded characters
    encoded_url = "https://example.com/test%20path%3Fparam%3Dvalue"
    decoded_url = "https://example.com/test path?param=value"

    # Calculate signature with decoded URL
    raw_string = f"GET{decoded_url}{current_timestamp}"
    expected_signature = hmac.new(
        "test_secret".encode(), raw_string.encode(), hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(expected_signature).decode()

    result = await verifier.verify_request(
        method="GET",
        url=encoded_url,
        body="",
        timestamp=current_timestamp,
        signature=expected_signature,
    )
    assert result is True


@pytest.mark.asyncio
async def test_verify_request_missing_timestamp():
    """Test verification fails when timestamp is missing."""
    verifier = HubSpotRequestVerifier("test-secret")
    result = await verifier.verify_request(
        method="POST",
        url="/webhook",
        body="test-body",
        timestamp="",  # Empty timestamp
        signature="test-signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_expired_timestamp():
    """Test verification fails when timestamp is expired."""
    verifier = HubSpotRequestVerifier("test-secret")
    result = await verifier.verify_request(
        method="POST",
        url="/webhook",
        body="test-body",
        timestamp="1000",  # Very old timestamp
        signature="test-signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_invalid_signature():
    """Test verification fails when signature is invalid."""
    verifier = HubSpotRequestVerifier("test-secret")
    result = await verifier.verify_request(
        method="POST",
        url="/webhook",
        body="test-body",
        timestamp="9999999999999",  # Future timestamp
        signature="invalid-signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_url_decoding():
    """Test verification with URL-encoded characters."""
    verifier = HubSpotRequestVerifier("test-secret")
    result = await verifier.verify_request(
        method="POST",
        url="/webhook%2Ftest%20path",  # URL-encoded path
        body="test-body",
        timestamp="9999999999999",  # Future timestamp
        signature="test-signature",
    )
    assert result is False


@pytest.mark.asyncio
async def test_verify_request_valid():
    """Test verification succeeds with valid parameters."""
    verifier = HubSpotRequestVerifier("test-secret")

    # Create a valid signature
    method = "POST"
    url = "/webhook"
    body = "test-body"
    timestamp = "9999999999999"  # Future timestamp

    # Create the string to hash
    raw_string = f"{method}{url}{body}{timestamp}"

    # Create HMAC SHA-256 hash and base64 encode it
    import hmac
    import hashlib
    import base64

    computed_signature = hmac.new(
        "test-secret".encode(), raw_string.encode(), hashlib.sha256
    ).digest()
    signature = base64.b64encode(computed_signature).decode()

    result = await verifier.verify_request(
        method=method, url=url, body=body, timestamp=timestamp, signature=signature
    )
    assert result is True
