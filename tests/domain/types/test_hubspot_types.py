import pytest

from src.domain.types.hubspot import UserInfo, Company


class TestUserInfo:
    """Test cases for UserInfo domain type."""

    def test_create_from_dict(self):
        """Test creating UserInfo from dictionary."""
        data = {
            "user_id": "123",
            "hub_id": 456,
            "app_id": 789,
            "user": "test@example.com",
            "scopes": ["contacts", "companies"],
            "token_type": "bearer",
            "expires_in": 3600,
            "token": "test_token",
        }

        user_info = UserInfo.from_dict(data)

        assert user_info.user_id == "123"
        assert user_info.hub_id == 456
        assert user_info.app_id == 789
        assert user_info.user_email == "test@example.com"
        assert user_info.scopes == ["contacts", "companies"]
        assert user_info.token_type == "bearer"
        assert user_info.expires_in == 3600
        assert user_info.token == "test_token"

    def test_create_from_dict_missing_optional_fields(self):
        """Test creating UserInfo with missing optional fields."""
        data = {
            "user_id": "123",
            "hub_id": 456,
            "app_id": 789,
            "user": "test@example.com",
            "scopes": ["contacts", "companies"],
            "token_type": "bearer",
            "expires_in": 3600,
        }

        user_info = UserInfo.from_dict(data)

        assert user_info.token is None

    def test_create_from_dict_missing_required_fields(self):
        """Test creating UserInfo with missing required fields."""
        data = {
            "user_id": "123",
            "hub_id": 456,
            "app_id": 789,
            "user": "test@example.com",
            "scopes": ["contacts", "companies"],
            "token_type": "bearer",
        }

        with pytest.raises(TypeError):
            UserInfo.from_dict(data)


class TestCompany:
    """Test cases for Company domain type."""

    def test_create_from_dict(self):
        """Test creating Company from dictionary."""
        data = {
            "id": "123",
            "name": "Test Company",
            "domain": "test.com",
            "industry": "Technology",
            "phone": "123-456-7890",
            "associated": True,
        }

        company = Company.from_dict(data)

        assert company.id == "123"
        assert company.name == "Test Company"
        assert company.domain == "test.com"
        assert company.industry == "Technology"
        assert company.phone == "123-456-7890"
        assert company.associated is True

    def test_create_from_dict_missing_optional_fields(self):
        """Test creating Company with missing optional fields."""
        data = {
            "id": "123",
            "name": "Test Company",
        }

        company = Company.from_dict(data)

        assert company.domain is None
        assert company.industry is None
        assert company.phone is None
        assert company.associated is False

    def test_create_from_dict_missing_required_fields(self):
        """Test creating Company with missing required fields."""
        data = {
            "id": "123",
        }

        with pytest.raises(TypeError):
            Company.from_dict(data)
