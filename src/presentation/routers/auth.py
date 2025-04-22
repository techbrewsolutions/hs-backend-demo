from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from src.domain.interfaces.hubspot import IHubSpotAuth
from src.domain.interfaces.repository import IHubSpotOAuthRepository
from src.infrastructure.hubspot.auth import HubSpotAuth
from src.infrastructure.repositories.file_repository import FileHubSpotOAuthRepository
from src.application.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize services
auth_client: IHubSpotAuth = HubSpotAuth()
repository: IHubSpotOAuthRepository = FileHubSpotOAuthRepository()
auth_service = AuthService(auth_client, repository)


@router.get("/install")
async def install() -> RedirectResponse:
    """Redirect to HubSpot OAuth login page."""
    try:
        auth_url = auth_client.get_authorization_url()
        return RedirectResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/callback")
async def hubspot_callback(code: str) -> dict[str, str]:
    """Handle HubSpot OAuth callback."""
    try:
        user_info = await auth_service.handle_oauth_callback(code)
        return {
            "status": "success",
            "message": "Authorization successful",
            "hub_id": str(user_info.hub_id),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
