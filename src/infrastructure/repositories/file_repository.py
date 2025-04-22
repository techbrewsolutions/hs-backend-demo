"""File-based repository implementation."""

import json
import os
from typing import Optional

from src.domain.interfaces.repository import IHubSpotOAuthRepository
from src.domain.types.hubspot import HubSpotOAuthData
from src.domain.exceptions import HubSpotOperationError


class FileHubSpotOAuthRepository(IHubSpotOAuthRepository):
    """File-based implementation of HubSpot OAuth repository."""

    def __init__(self, storage_dir: str = ".data/auth"):
        """Initialize repository with storage directory.

        Args:
            storage_dir (str): The directory to store the OAuth data.
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists.

        Raises:
            HubSpotOperationError: If the storage directory cannot be created.
        """
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_file_path(self, hub_id: str) -> str:
        """Get file path for a hub ID.

        Args:
            hub_id (str): The hub ID of the OAuth data to get.

        Returns:
            str: The file path.
        """
        return os.path.join(self.storage_dir, f"hubspot_auth_{hub_id}.json")

    async def save(self, data: HubSpotOAuthData) -> None:
        """Save HubSpot OAuth data to file.

        Args:
            data (HubSpotOAuthData): The HubSpot OAuth data to save.
        """
        try:
            file_path = self._get_file_path(data.hub_id)
            with open(file_path, "w") as f:
                json.dump(data.to_dict(), f, indent=2)
        except Exception as e:
            raise HubSpotOperationError(f"Failed to save OAuth data: {str(e)}")

    async def get_by_hub_id(self, hub_id: str) -> Optional[HubSpotOAuthData]:
        """Get HubSpot OAuth data by hub ID from file.

        Args:
            hub_id (str): The hub ID of the OAuth data to get.

        Returns:
            Optional[HubSpotOAuthData]: The HubSpot OAuth data.
        """
        try:
            file_path = self._get_file_path(hub_id)
            if not os.path.exists(file_path):
                return None

            with open(file_path, "r") as f:
                data = json.load(f)
                return HubSpotOAuthData.from_dict(data)
        except Exception as e:
            raise HubSpotOperationError(f"Failed to get OAuth data: {str(e)}")

    async def update(self, data: HubSpotOAuthData) -> None:
        """Update existing HubSpot OAuth data in file.

        Args:
            data (HubSpotOAuthData): The HubSpot OAuth data to update.
        """
        try:
            file_path = self._get_file_path(data.hub_id)
            if not os.path.exists(file_path):
                raise HubSpotOperationError(
                    f"No OAuth data found for hub ID: {data.hub_id}"
                )

            with open(file_path, "w") as f:
                json.dump(data.to_dict(), f, indent=2)
        except Exception as e:
            raise HubSpotOperationError(f"Failed to update OAuth data: {str(e)}")

    async def delete(self, hub_id: str) -> None:
        """Delete HubSpot OAuth data by hub ID from file.

        Args:
            hub_id (str): The hub ID of the OAuth data to delete.
        """
        try:
            file_path = self._get_file_path(hub_id)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise HubSpotOperationError(f"Failed to delete OAuth data: {str(e)}")
