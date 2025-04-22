from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

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

# Initialize templates
templates = Jinja2Templates(directory="src/presentation/templates")


@router.get("/install")
async def install() -> RedirectResponse:
    """Redirect to HubSpot OAuth login page."""
    try:
        auth_url = auth_client.get_authorization_url()
        return RedirectResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/callback")
async def hubspot_callback(
    request: Request,
    code: str,
    redirect_uri: Optional[str] = None,
) -> Response:
    """Handle HubSpot OAuth callback and show success/error page before redirecting to HubSpot."""
    try:
        user_info = await auth_service.handle_oauth_callback(code)

        # Default redirect URI if not provided
        if not redirect_uri:
            redirect_uri = (
                f"https://app.hubspot.com/contacts/{user_info.hub_id}/dashboard"
            )

        # Add success message to the redirect URL
        success_url = f"{redirect_uri}?app_install_success=true"

        # Return the success page template
        return templates.TemplateResponse(
            "success.html",
            {"request": request, "redirect_url": success_url},
        )
    except Exception as e:
        # If there's an error, show error page
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": str(e),
            },
        )
