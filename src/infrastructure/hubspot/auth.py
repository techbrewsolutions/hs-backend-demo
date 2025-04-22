import httpx
from typing import Dict, Any

from src.domain.interfaces.hubspot import IHubSpotAuth
from src.domain.types.hubspot import UserInfo
from src.domain.exceptions import HubSpotAuthenticationError, HubSpotOperationError
from src.infrastructure.config import get_settings

settings = get_settings()


class HubSpotAuth(IHubSpotAuth):
    """Implementation of HubSpot authentication operations."""

    AUTH_URL = "https://app.hubspot.com/oauth/authorize"
    TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"
    USER_INFO_URL = "https://api.hubapi.com/oauth/v1/access-tokens/"

    def get_authorization_url(self) -> str:
        """Get the authorization URL for the HubSpot OAuth flow.

        Returns:
            str: The authorization URL.
        """
        params = {
            "client_id": settings.HUBSPOT_CLIENT_ID,
            "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
            "scope": settings.HUBSPOT_SCOPES,
        }
        return f"{self.AUTH_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    async def get_access_token(self, code: str) -> Dict[str, Any]:
        """Get the access token for the HubSpot OAuth flow.

        Args:
            code (str): The authorization code.

        Returns:
            Dict[str, Any]: The access token.

        Raises:
            HubSpotAuthenticationError: If the authorization code is invalid.
            HubSpotOperationError: If the access token cannot be retrieved.
        """
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "authorization_code",
                "client_id": settings.HUBSPOT_CLIENT_ID,
                "client_secret": settings.HUBSPOT_CLIENT_SECRET,
                "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
                "code": code,
            }

            try:
                response = await client.post(self.TOKEN_URL, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                if response.status_code == 400:
                    raise HubSpotAuthenticationError(
                        f"Invalid authorization code: {str(e)}"
                    )
                raise HubSpotOperationError(f"Failed to get access token: {str(e)}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh the access token for the HubSpot OAuth flow.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            Dict[str, Any]: The access token.

        Raises:
            HubSpotAuthenticationError: If the refresh token is invalid.
            HubSpotOperationError: If the access token cannot be refreshed.
        """
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "refresh_token",
                "client_id": settings.HUBSPOT_CLIENT_ID,
                "client_secret": settings.HUBSPOT_CLIENT_SECRET,
                "refresh_token": refresh_token,
            }

            try:
                response = await client.post(self.TOKEN_URL, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                if response.status_code == 400:
                    raise HubSpotAuthenticationError(f"Invalid refresh token: {str(e)}")
                raise HubSpotOperationError(f"Failed to refresh token: {str(e)}")

    async def get_user_info(self, access_token: str) -> UserInfo:
        """Get the user info for the HubSpot OAuth flow.

        Args:
            access_token (str): The access token.

        Returns:
            UserInfo: The user info.

        Raises:
            HubSpotAuthenticationError: If the access token is invalid.
            HubSpotOperationError: If the user info cannot be retrieved.
        """
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            try:
                response = await client.get(
                    f"{self.USER_INFO_URL}{access_token}", headers=headers
                )
                response.raise_for_status()
                data = response.json()
                return UserInfo.from_dict(data)
            except httpx.HTTPError as e:
                if response.status_code == 401:
                    raise HubSpotAuthenticationError(f"Invalid access token: {str(e)}")
                raise HubSpotOperationError(f"Failed to get user info: {str(e)}")
