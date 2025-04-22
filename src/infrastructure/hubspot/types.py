from pydantic import BaseModel
from hubspot.crm.companies.models import BatchReadInputSimplePublicObjectId


class Contact(BaseModel):
    """A contact in HubSpot."""

    id: str
    name: str
    email: str
    phone: str


# Type alias for HubSpot company batch input
CompanyBatchInput = BatchReadInputSimplePublicObjectId
