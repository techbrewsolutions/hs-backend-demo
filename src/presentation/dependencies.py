"""FastAPI dependencies."""

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Query
from typing import Annotated

from src.domain.interfaces.repository import IHubSpotOAuthRepository
from src.domain.interfaces.hubspot import IHubSpotAuth
from src.domain.types.hubspot import HubSpotOAuthData
from src.infrastructure.repositories.file_repository import FileHubSpotOAuthRepository
from src.infrastructure.hubspot.auth import HubSpotAuth
from src.domain.exceptions import HubSpotOperationError

# Initialize services
repository: IHubSpotOAuthRepository = FileHubSpotOAuthRepository()
auth_client: IHubSpotAuth = HubSpotAuth()


async def get_oauth_data(
    portal_id: Annotated[str, Query(alias="portalId", description="HubSpot portal ID")],
) -> HubSpotOAuthData:
    """Dependency to get OAuth data for a portal.

    Args:
        portal_id: The HubSpot portal ID

    Returns:
        HubSpotOAuthData: The OAuth data for the portal

    Raises:
        HTTPException: If OAuth data is not found or token refresh fails
    """
    oauth_data = await repository.get_by_hub_id(portal_id)
    if not oauth_data:
        raise HTTPException(
            status_code=401,
            detail="Unable to access HubSpot data. Please ensure the app is properly installed.",
        )

    # Check if token is expired or about to expire (within 5 minutes)
    if datetime.now() >= oauth_data.expires_at:
        try:
            # Refresh the token
            token_response = await auth_client.refresh_access_token(
                oauth_data.refresh_token
            )

            # Update OAuth data with new tokens
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

            # Save updated data
            await repository.update(updated_data)
            return updated_data
        except HubSpotOperationError as e:
            raise HTTPException(
                status_code=401,
                detail="Failed to refresh access token. Please reinstall the app.",
            )

    return oauth_data
