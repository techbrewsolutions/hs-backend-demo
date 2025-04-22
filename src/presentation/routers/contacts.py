from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from src.domain.interfaces.hubspot import IHubSpotContactService, IHubSpotCompanyService
from src.infrastructure.hubspot.contact_service import HubSpotContactService
from src.infrastructure.hubspot.company_service import HubSpotCompanyService
from src.domain.exceptions import HubSpotOperationError
from src.domain.types.hubspot import HubSpotOAuthData
from src.presentation.dependencies import get_oauth_data

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Initialize services
contact_service: IHubSpotContactService = HubSpotContactService()
company_service: IHubSpotCompanyService = HubSpotCompanyService()


@router.get("/")
async def get_contacts(
    oauth_data: HubSpotOAuthData = Depends(get_oauth_data),
    limit: int = 10,
    after: Optional[str] = None,
) -> List[dict]:
    """Get list of contacts."""
    try:
        # Get contacts using the access token
        contacts = await contact_service.get_contacts(
            access_token=oauth_data.access_token, limit=limit, after=after
        )

        return [contact.to_dict() for contact in contacts]
    except HubSpotOperationError as e:
        raise HTTPException(
            status_code=400, detail="Failed to fetch contacts from HubSpot"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/{contact_id}/companies")
async def get_contact_companies(
    contact_id: str, oauth_data: HubSpotOAuthData = Depends(get_oauth_data)
) -> List[dict]:
    """Get companies associated with a contact."""
    try:
        # Get companies using the access token
        companies = await company_service.get_companies_associated_with_contact(
            access_token=oauth_data.access_token, contact_id=contact_id
        )
        return [company.to_dict() for company in companies]
    except HubSpotOperationError as e:
        raise HTTPException(
            status_code=400, detail="Failed to fetch companies from HubSpot"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.post("/{contact_id}/companies/{company_id}")
async def add_company_association(
    contact_id: str,
    company_id: str,
    oauth_data: HubSpotOAuthData = Depends(get_oauth_data),
) -> dict:
    """Add a company association to a contact."""
    try:
        await company_service.create_association(
            oauth_data.access_token,
            contact_id,
            company_id,
        )

        return {
            "status": "success",
            "message": "Company association added successfully",
        }
    except HubSpotOperationError as e:
        raise HTTPException(status_code=400, detail="Failed to add company association")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/{contact_id}/companies/{company_id}")
async def remove_company_association(
    contact_id: str,
    company_id: str,
    oauth_data: HubSpotOAuthData = Depends(get_oauth_data),
) -> dict:
    """Remove a company association from a contact."""
    try:
        await company_service.remove_association(
            oauth_data.access_token,
            contact_id,
            company_id,
        )

        return {
            "status": "success",
            "message": "Company association removed successfully",
        }
    except HubSpotOperationError as e:
        raise HTTPException(
            status_code=400, detail="Failed to remove company association"
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
