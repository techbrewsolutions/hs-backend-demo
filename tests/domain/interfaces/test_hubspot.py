"""Tests for HubSpot interfaces."""

import pytest
from typing import List, Optional

from src.domain.interfaces.hubspot import (
    IHubSpotAuth,
    IHubSpotContactService,
    IHubSpotCompanyService,
)
from src.domain.types.hubspot import UserInfo, Company
from src.infrastructure.hubspot.types import Contact


class MockHubSpotAuth(IHubSpotAuth):
    """Mock implementation of IHubSpotAuth for testing."""

    def get_authorization_url(self) -> str:
        return "https://mock-auth-url"

    async def get_access_token(self, code: str) -> dict:
        return {"access_token": "mock-token"}

    async def refresh_access_token(self, refresh_token: str) -> dict:
        return {"access_token": "new-mock-token"}

    async def get_user_info(self, access_token: str) -> UserInfo:
        return UserInfo(
            user_id="123",
            hub_id=456,
            app_id=789,
            user_email="test@example.com",
            scopes=["contacts"],
            token_type="bearer",
            expires_in=3600,
        )


class MockHubSpotContactService(IHubSpotContactService):
    """Mock implementation of IHubSpotContactService for testing."""

    async def get_contacts(
        self, access_token: str, limit: int = 10, after: Optional[str] = None
    ) -> List[Contact]:
        return [
            Contact(
                id="123",
                name="Test Contact",
                email="test@example.com",
                phone="123-456-7890",
            )
        ]


class MockHubSpotCompanyService(IHubSpotCompanyService):
    """Mock implementation of IHubSpotCompanyService for testing."""

    async def get_companies_associated_with_contact(
        self, access_token: str, contact_id: str, limit: int = 10
    ) -> List[Company]:
        return [Company(id="456", name="Test Company")]

    async def create_association(
        self, access_token: str, contact_id: str, company_id: str
    ) -> None:
        pass

    async def remove_association(
        self, access_token: str, contact_id: str, company_id: str
    ) -> None:
        pass


@pytest.mark.asyncio
class TestHubSpotInterfaces:
    """Test cases for HubSpot interfaces."""

    async def test_auth_interface(self):
        """Test IHubSpotAuth interface methods."""
        auth = MockHubSpotAuth()

        # Test get_authorization_url
        auth_url = auth.get_authorization_url()
        assert auth_url == "https://mock-auth-url"

        # Test get_access_token
        token_response = await auth.get_access_token("test-code")
        assert token_response["access_token"] == "mock-token"

        # Test refresh_access_token
        refresh_response = await auth.refresh_access_token("old-token")
        assert refresh_response["access_token"] == "new-mock-token"

        # Test get_user_info
        user_info = await auth.get_user_info("test-token")
        assert isinstance(user_info, UserInfo)
        assert user_info.user_id == "123"

    async def test_contact_service_interface(self):
        """Test IHubSpotContactService interface methods."""
        contact_service = MockHubSpotContactService()

        # Test get_contacts with default parameters
        contacts = await contact_service.get_contacts("test-token")
        assert len(contacts) == 1
        assert contacts[0].id == "123"
        assert contacts[0].email == "test@example.com"
        assert contacts[0].name == "Test Contact"
        assert contacts[0].phone == "123-456-7890"

        # Test get_contacts with custom limit and after
        contacts = await contact_service.get_contacts(
            "test-token", limit=5, after="last-contact-id"
        )
        assert len(contacts) == 1

    async def test_company_service_interface(self):
        """Test IHubSpotCompanyService interface methods."""
        company_service = MockHubSpotCompanyService()

        # Test get_companies_associated_with_contact with default limit
        companies = await company_service.get_companies_associated_with_contact(
            "test-token", "123"
        )
        assert len(companies) == 1
        assert companies[0].id == "456"
        assert companies[0].name == "Test Company"

        # Test get_companies_associated_with_contact with custom limit
        companies = await company_service.get_companies_associated_with_contact(
            "test-token", "123", limit=5
        )
        assert len(companies) == 1

        # Test create_association
        await company_service.create_association("test-token", "123", "456")

        # Test remove_association
        await company_service.remove_association("test-token", "123", "456")
