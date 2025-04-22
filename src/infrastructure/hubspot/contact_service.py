from typing import List, Optional
import httpx

from src.domain.interfaces.hubspot import IHubSpotContactService
from src.domain.types.hubspot import Contact
from src.domain.exceptions import HubSpotAuthenticationError, HubSpotOperationError
from src.infrastructure.config import get_settings

settings = get_settings()


class HubSpotContactService(IHubSpotContactService):
    """Implementation of HubSpot contact operations."""

    CONTACTS_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

    async def get_contacts(
        self, access_token: str, limit: int = 10, after: Optional[str] = None
    ) -> List[Contact]:
        """Get contacts from HubSpot.

        Args:
            access_token (str): The access token.
            limit (int): The maximum number of contacts to return.
            after (Optional[str]): The ID of the last contact to return.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "limit": limit,
            "properties": ["firstname", "lastname", "email", "phone"],
        }
        if after:
            params["after"] = after

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.CONTACTS_URL, headers=headers, params=params
                )
                response.raise_for_status()
                data = response.json()

                contacts = []
                for result in data.get("results", []):
                    properties = result.get("properties", {})
                    contact = Contact(
                        id=result["id"],
                        name=f"{properties.get('firstname', '')} {properties.get('lastname', '')}".strip(),
                        email=properties.get("email", ""),
                        phone=properties.get("phone", ""),
                    )
                    contacts.append(contact)
                return contacts
            except httpx.HTTPError as e:
                if response.status_code == 401:
                    raise HubSpotAuthenticationError(f"Invalid access token: {str(e)}")
                raise HubSpotOperationError(f"Failed to get contacts: {str(e)}")
