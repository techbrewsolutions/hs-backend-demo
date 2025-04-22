"""Repository interfaces for data persistence."""

from typing import Optional, Protocol

from src.domain.types.hubspot import HubSpotOAuthData


class IHubSpotOAuthRepository(Protocol):
    """Interface for HubSpot OAuth data persistence."""

    async def save(self, data: HubSpotOAuthData) -> None:
        """Save HubSpot OAuth data to the database.

        Args:
            data (HubSpotOAuthData): The HubSpot OAuth data to save.
        """
        ...

    async def get_by_hub_id(self, hub_id: str) -> Optional[HubSpotOAuthData]:
        """Get HubSpot OAuth data by hub ID from the database.

        Args:
            hub_id (str): The hub ID of the HubSpot OAuth data to get.

        Returns:
            Optional[HubSpotOAuthData]: The HubSpot OAuth data.
        """
        ...

    async def update(self, data: HubSpotOAuthData) -> None:
        """Update existing HubSpot OAuth data in the database.

        Args:
            data (HubSpotOAuthData): The HubSpot OAuth data to update.
        """
        ...

    async def delete(self, hub_id: str) -> None:
        """Delete HubSpot OAuth data by hub ID from the database.

        Args:
            hub_id (str): The hub ID of the HubSpot OAuth data to delete.
        """
        ...
