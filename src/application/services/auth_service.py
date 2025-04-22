"""Authentication service implementation."""

from datetime import datetime, timedelta

from src.domain.interfaces.hubspot import IHubSpotAuth
from src.domain.interfaces.repository import IHubSpotOAuthRepository
from src.domain.types.hubspot import HubSpotOAuthData, UserInfo
from src.domain.exceptions import HubSpotOperationError


class AuthService:
    """Authentication service for HubSpot OAuth."""

    def __init__(
        self,
        auth_client: IHubSpotAuth,
        repository: IHubSpotOAuthRepository,
    ):
        """Initialize auth service with client and repository."""
        self.auth_client = auth_client
        self.repository = repository

    async def handle_oauth_callback(self, code: str) -> UserInfo:
        """Handle OAuth callback and store tokens."""
        try:
            # Get access token from HubSpot
            token_response = await self.auth_client.get_access_token(code)

            # Get user info using the access token
            user_info = await self.auth_client.get_user_info(
                token_response["access_token"]
            )

            # Create OAuth data
            oauth_data = HubSpotOAuthData(
                hub_id=str(user_info.hub_id),
                access_token=token_response["access_token"],
                refresh_token=token_response["refresh_token"],
                expires_at=datetime.now()
                + timedelta(seconds=token_response["expires_in"]),
                scopes=user_info.scopes,
                installed_at=datetime.now(),
                user_id=user_info.user_id,
                app_id=str(user_info.app_id),
            )

            # Save OAuth data
            await self.repository.save(oauth_data)

            return user_info
        except Exception as e:
            raise HubSpotOperationError(f"Failed to handle OAuth callback: {str(e)}")

    async def refresh_token(self, hub_id: str) -> None:
        """Refresh access token for a HubSpot installation."""
        try:
            # Get existing OAuth data
            oauth_data = await self.repository.get_by_hub_id(hub_id)
            if not oauth_data:
                raise HubSpotOperationError(f"No OAuth data found for hub ID: {hub_id}")

            # Refresh token
            token_response = await self.auth_client.refresh_token(
                oauth_data.refresh_token
            )

            # Update OAuth data
            updated_data = HubSpotOAuthData(
                hub_id=oauth_data.hub_id,
                access_token=token_response["access_token"],
                refresh_token=token_response["refresh_token"],
                expires_at=datetime.now()
                + timedelta(seconds=token_response["expires_in"]),
                scopes=oauth_data.scopes,
                installed_at=oauth_data.installed_at,
                user_id=oauth_data.user_id,
                app_id=oauth_data.app_id,
            )

            await self.repository.update(updated_data)
        except Exception as e:
            raise HubSpotOperationError(f"Failed to refresh token: {str(e)}")
