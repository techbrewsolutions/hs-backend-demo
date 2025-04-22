"""Tests for file-based repository implementation."""

import os
import json
import pytest
from datetime import datetime, timedelta

from src.infrastructure.repositories.file_repository import FileHubSpotOAuthRepository
from src.domain.types.hubspot import HubSpotOAuthData
from src.domain.exceptions import HubSpotOperationError


@pytest.fixture
def repository(tmp_path):
    """Create a repository instance with temporary directory."""
    return FileHubSpotOAuthRepository(storage_dir=str(tmp_path))


@pytest.fixture
def sample_oauth_data():
    """Create sample OAuth data."""
    return HubSpotOAuthData(
        hub_id="123",
        access_token="test_access_token",
        refresh_token="test_refresh_token",
        expires_at=datetime.now() + timedelta(hours=1),
        scopes=["contacts", "companies"],
        installed_at=datetime.now(),
        user_id="user123",
        app_id="app123",
    )


@pytest.mark.asyncio
async def test_save_and_get(repository, sample_oauth_data):
    """Test saving and retrieving OAuth data."""
    # Save data
    await repository.save(sample_oauth_data)

    # Retrieve data
    retrieved_data = await repository.get_by_hub_id(sample_oauth_data.hub_id)

    assert retrieved_data is not None
    assert retrieved_data.hub_id == sample_oauth_data.hub_id
    assert retrieved_data.access_token == sample_oauth_data.access_token
    assert retrieved_data.refresh_token == sample_oauth_data.refresh_token
    assert retrieved_data.scopes == sample_oauth_data.scopes
    assert retrieved_data.user_id == sample_oauth_data.user_id
    assert retrieved_data.app_id == sample_oauth_data.app_id


@pytest.mark.asyncio
async def test_get_nonexistent(repository):
    """Test retrieving non-existent data."""
    retrieved_data = await repository.get_by_hub_id("nonexistent")
    assert retrieved_data is None


@pytest.mark.asyncio
async def test_update(repository, sample_oauth_data):
    """Test updating OAuth data."""
    # Save initial data
    await repository.save(sample_oauth_data)

    # Update data
    updated_data = HubSpotOAuthData(
        hub_id=sample_oauth_data.hub_id,
        access_token="new_access_token",
        refresh_token="new_refresh_token",
        expires_at=datetime.now() + timedelta(hours=2),
        scopes=["contacts"],
        installed_at=datetime.now(),
        user_id="user123",
        app_id="app123",
    )
    await repository.update(updated_data)

    # Retrieve updated data
    retrieved_data = await repository.get_by_hub_id(sample_oauth_data.hub_id)

    assert retrieved_data is not None
    assert retrieved_data.access_token == "new_access_token"
    assert retrieved_data.refresh_token == "new_refresh_token"
    assert retrieved_data.scopes == ["contacts"]


@pytest.mark.asyncio
async def test_update_nonexistent(repository, sample_oauth_data):
    """Test updating non-existent data."""
    with pytest.raises(HubSpotOperationError):
        await repository.update(sample_oauth_data)


@pytest.mark.asyncio
async def test_delete(repository, sample_oauth_data):
    """Test deleting OAuth data."""
    # Save data
    await repository.save(sample_oauth_data)

    # Delete data
    await repository.delete(sample_oauth_data.hub_id)

    # Verify deletion
    retrieved_data = await repository.get_by_hub_id(sample_oauth_data.hub_id)
    assert retrieved_data is None


@pytest.mark.asyncio
async def test_delete_nonexistent(repository):
    """Test deleting non-existent data."""
    # Should not raise an error
    await repository.delete("nonexistent")


@pytest.mark.asyncio
async def test_save_invalid_data(repository, tmp_path):
    """Test saving invalid data."""
    # Create invalid file
    invalid_file = os.path.join(tmp_path, "hubspot_auth_123.json")
    with open(invalid_file, "w") as f:
        json.dump({"invalid": "data"}, f)

    # Try to read invalid data
    with pytest.raises(HubSpotOperationError):
        await repository.get_by_hub_id("123")


@pytest.mark.asyncio
async def test_save_permission_error(repository, tmp_path):
    """Test handling permission errors."""
    # Make directory read-only
    os.chmod(tmp_path, 0o444)

    with pytest.raises(HubSpotOperationError):
        await repository.save(
            HubSpotOAuthData(
                hub_id="123",
                access_token="test",
                refresh_token="test",
                expires_at=datetime.now(),
                scopes=[],
                installed_at=datetime.now(),
                user_id="user123",
                app_id="app123",
            )
        )
