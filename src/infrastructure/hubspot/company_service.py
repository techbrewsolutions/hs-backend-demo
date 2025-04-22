from typing import List

from hubspot import HubSpot
from hubspot.crm.associations.v4.models import AssociationSpec

from src.domain.exceptions import HubSpotOperationError
from src.domain.interfaces.hubspot import IHubSpotCompanyService
from src.domain.types.hubspot import Company


class HubSpotCompanyService(IHubSpotCompanyService):
    """Implementation of HubSpot company operations."""

    async def get_companies_associated_with_contact(
        self, access_token: str, contact_id: str, limit: int = 10
    ) -> List[Company]:
        """Get companies associated with a contact.

        Args:
            access_token (str): The access token.
            contact_id (str): The ID of the contact.
            limit (int): The maximum number of companies to return.
        """
        try:
            api_client = HubSpot(access_token=access_token)

            # Get associated companies using the v4 associations API
            associations = api_client.crm.associations.v4.basic_api.get_page(
                object_type="contacts",
                object_id=contact_id,
                to_object_type="companies",
                limit=limit,
            )

            if not associations.results:
                return []

            # Get company IDs from associations
            company_ids = [assoc.to_object_id for assoc in associations.results]

            from hubspot.crm.companies.models import BatchReadInputSimplePublicObjectId

            batch_input = BatchReadInputSimplePublicObjectId(
                inputs=[{"id": id} for id in company_ids]
            )
            # Get all company details in a single batch request
            companies_response = api_client.crm.companies.batch_api.read(
                batch_read_input_simple_public_object_id=batch_input,
            )

            # Format the response
            companies = []
            for company in companies_response.results:
                companies.append(
                    Company.from_dict(
                        {
                            "id": company.id,
                            "name": company.properties.get("name"),
                            "domain": company.properties.get("domain"),
                            "industry": company.properties.get("industry"),
                            "phone": company.properties.get("phone"),
                            "associated": True,
                        }
                    )
                )

            return companies
        except Exception as e:
            raise HubSpotOperationError(f"Failed to get companies: {str(e)}")

    async def create_association(
        self,
        access_token: str,
        contact_id: str,
        company_id: str,
    ) -> None:
        """Create association between contact and company.

        Args:
            access_token (str): The access token.
            contact_id (str): The ID of the contact.
            company_id (str): The ID of the company.
        """
        try:
            api_client = HubSpot(access_token=access_token)
            api_client.crm.associations.v4.basic_api.create(
                object_type="contacts",
                object_id=contact_id,
                to_object_type="companies",
                to_object_id=company_id,
                association_spec=[
                    AssociationSpec(
                        association_category="HUBSPOT_DEFINED",
                        association_type_id=1,
                    )
                ],
            )
        except Exception as e:
            raise HubSpotOperationError(f"Failed to create association: {str(e)}")

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
        try:
            api_client = HubSpot(access_token=access_token)
            api_client.crm.associations.v4.basic_api.archive(
                object_type="contacts",
                object_id=contact_id,
                to_object_type="companies",
                to_object_id=company_id,
            )
        except Exception as e:
            raise HubSpotOperationError(f"Failed to remove association: {str(e)}")
