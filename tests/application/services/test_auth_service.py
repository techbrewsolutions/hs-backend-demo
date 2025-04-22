"""Tests for authentication service."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from src.application.services.auth_service import AuthService
from src.domain.types.hubspot import HubSpotOAuthData, UserInfo
from src.domain.exceptions import HubSpotOperationError


@pytest.fixture
def mock_auth_client():
    """Create a mock auth client."""
    client = AsyncMock()
    client.get_access_token.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
    }
    client.get_user_info.return_value = UserInfo(
        user_id="user123",
        hub_id=123,
        app_id=456,
        user_email="test@example.com",
        scopes=["contacts", "companies"],
        token_type="bearer",
        expires_in=3600,
    )
    client.refresh_token.return_value = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "expires_in": 3600,
    }
    return client


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    repository = AsyncMock()
    repository.get_by_hub_id.return_value = HubSpotOAuthData(
        hub_id="123",
        access_token="old_access_token",
        refresh_token="old_refresh_token",
        expires_at=datetime.now() - timedelta(hours=1),
        scopes=["contacts", "companies"],
        installed_at=datetime.now() - timedelta(days=1),
        user_id="user123",
        app_id="app123",
    )
    return repository


@pytest.fixture
def auth_service(mock_auth_client, mock_repository):
    """Create an auth service with mocked dependencies."""
    return AuthService(mock_auth_client, mock_repository)


@pytest.mark.asyncio
async def test_handle_oauth_callback_success(
    auth_service, mock_auth_client, mock_repository
):
    """Test successful OAuth callback handling."""
    # Call the service
    user_info = await auth_service.handle_oauth_callback("test_code")

    # Verify auth client calls
    mock_auth_client.get_access_token.assert_called_once_with("test_code")
    mock_auth_client.get_user_info.assert_called_once_with("test_access_token")

    # Verify repository save
    mock_repository.save.assert_called_once()
    saved_data = mock_repository.save.call_args[0][0]
    assert isinstance(saved_data, HubSpotOAuthData)
    assert saved_data.hub_id == "123"
    assert saved_data.access_token == "test_access_token"
    assert saved_data.refresh_token == "test_refresh_token"

    # Verify returned user info
    assert isinstance(user_info, UserInfo)
    assert user_info.user_id == "user123"
    assert user_info.hub_id == 123


@pytest.mark.asyncio
async def test_handle_oauth_callback_auth_error(auth_service, mock_auth_client):
    """Test OAuth callback handling with auth error."""
    # Make auth client raise an error
    mock_auth_client.get_access_token.side_effect = Exception("Auth error")

    # Verify error is raised
    with pytest.raises(HubSpotOperationError):
        await auth_service.handle_oauth_callback("test_code")


@pytest.mark.asyncio
async def test_refresh_token_success(auth_service, mock_auth_client, mock_repository):
    """Test successful token refresh."""
    # Call the service
    await auth_service.refresh_token("123")

    # Verify repository get
    mock_repository.get_by_hub_id.assert_called_once_with("123")

    # Verify auth client refresh
    mock_auth_client.refresh_token.assert_called_once_with("old_refresh_token")

    # Verify repository update
    mock_repository.update.assert_called_once()
    updated_data = mock_repository.update.call_args[0][0]
    assert isinstance(updated_data, HubSpotOAuthData)
    assert updated_data.hub_id == "123"
    assert updated_data.access_token == "new_access_token"
    assert updated_data.refresh_token == "new_refresh_token"


@pytest.mark.asyncio
async def test_refresh_token_not_found(auth_service, mock_repository):
    """Test token refresh with non-existent data."""
    # Make repository return None
    mock_repository.get_by_hub_id.return_value = None

    # Verify error is raised
    with pytest.raises(HubSpotOperationError):
        await auth_service.refresh_token("123")


@pytest.mark.asyncio
async def test_refresh_token_auth_error(auth_service, mock_auth_client):
    """Test token refresh with auth error."""
    # Make auth client raise an error
    mock_auth_client.refresh_token.side_effect = Exception("Auth error")

    # Verify error is raised
    with pytest.raises(HubSpotOperationError):
        await auth_service.refresh_token("123")
