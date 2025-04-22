"""Tests for domain exceptions."""

from src.domain.exceptions import (
    HubSpotException,
    HubSpotAuthenticationError,
    HubSpotOperationError,
)


def test_hubspot_exception():
    """Test HubSpotException can be raised with a message."""
    message = "Test error"
    try:
        raise HubSpotException(message)
    except HubSpotException as e:
        assert str(e) == message


def test_hubspot_authentication_error():
    """Test HubSpotAuthenticationError can be raised with a message."""
    message = "Authentication failed"
    try:
        raise HubSpotAuthenticationError(message)
    except HubSpotAuthenticationError as e:
        assert str(e) == message
        assert isinstance(e, HubSpotException)


def test_hubspot_operation_error():
    """Test HubSpotOperationError can be raised with a message."""
    message = "Operation failed"
    try:
        raise HubSpotOperationError(message)
    except HubSpotOperationError as e:
        assert str(e) == message
        assert isinstance(e, HubSpotException)
