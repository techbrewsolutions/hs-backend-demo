from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from src.domain.types.hubspot import UserInfo, Company, Contact


class IHubSpotAuth(Protocol):
    """Interface for HubSpot authentication operations."""

    def get_authorization_url(self) -> str:
        """Get the HubSpot OAuth authorization URL.

        Returns:
            str: The authorization URL.
        """
        ...

    async def get_access_token(self, code: str) -> dict:
        """Exchange authorization code for access token.

        Args:
            code (str): The authorization code.

        Returns:
            dict: The access token.
        """
        ...

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh an expired access token.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            dict: The access token.
        """
        ...

    async def get_user_info(self, access_token: str) -> UserInfo:
        """Get user information using the access token.

        Args:
            access_token (str): The access token.

        Returns:
            UserInfo: The user info.
        """
        ...


class IHubSpotContactService(ABC):
    """Interface for HubSpot contact operations."""

    @abstractmethod
    async def get_contacts(
        self, access_token: str, limit: int = 10, after: Optional[str] = None
    ) -> List[Contact]:
        """Get contacts from HubSpot.

        Args:
            access_token (str): The access token.
            limit (int): The maximum number of contacts to return.
            after (Optional[str]): The ID of the last contact to return.
        """
        pass


class IHubSpotCompanyService(ABC):
    """Interface for HubSpot company operations."""

    @abstractmethod
    async def get_companies_associated_with_contact(
        self, access_token: str, contact_id: str, limit: int = 10
    ) -> List[Company]:
        """Get companies associated with a contact.

        Args:
            access_token: OAuth access token
            contact_id: HubSpot contact ID
            limit: Maximum number of companies to retrieve (default: 10)
        """
        pass

    @abstractmethod
    async def create_association(
        self,
        access_token: str,
        contact_id: str,
        company_id: str,
    ) -> None:
        """Create association between contact and company.

        Args:
            access_token: OAuth access token
            contact_id: HubSpot contact ID
            company_id: HubSpot company ID
        """
        pass

    @abstractmethod
    async def remove_association(
        self,
        access_token: str,
        contact_id: str,
        company_id: str,
    ) -> None:
        """Remove association between contact and company.

        Args:
            access_token (str): The access token.
            contact_id (str): The ID of the contact.
            company_id (str): The ID of the company.
        """
        pass
