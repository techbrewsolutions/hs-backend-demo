from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class UserInfo:
    """User information from HubSpot OAuth."""

    user_id: str
    hub_id: int
    app_id: int
    user_email: str  # The email address from HubSpot's user field
    scopes: List[str]
    token_type: str
    expires_in: int
    token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UserInfo":
        """Create UserInfo from dictionary."""
        required_fields = {
            "user_id",
            "hub_id",
            "app_id",
            "user",  # HubSpot sends this as 'user' in the response
            "scopes",
            "token_type",
            "expires_in",
        }
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise TypeError(f"Missing required fields: {missing_fields}")

        return cls(
            user_id=data["user_id"],
            hub_id=data["hub_id"],
            app_id=data["app_id"],
            user_email=data["user"],  # Map HubSpot's 'user' field to user_email
            scopes=data["scopes"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            token=data.get("token"),
        )


@dataclass
class HubSpotOAuthData:
    """HubSpot OAuth data for an installation."""

    hub_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    scopes: str
    installed_at: datetime
    user_id: str
    app_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "HubSpotOAuthData":
        """Create HubSpotOAuthData from dictionary."""
        required_fields = {
            "hub_id",
            "access_token",
            "refresh_token",
            "expires_at",
            "scopes",
            "installed_at",
            "user_id",
            "app_id",
        }
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise TypeError(f"Missing required fields: {missing_fields}")

        return cls(
            hub_id=data["hub_id"],
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            scopes=data["scopes"],
            installed_at=datetime.fromisoformat(data["installed_at"]),
            user_id=data["user_id"],
            app_id=data["app_id"],
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "hub_id": self.hub_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat(),
            "scopes": self.scopes,
            "installed_at": self.installed_at.isoformat(),
            "user_id": self.user_id,
            "app_id": self.app_id,
        }


@dataclass
class Contact:
    """Contact information from HubSpot."""

    id: str
    name: str
    email: str
    phone: str

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """Create Contact from dictionary."""
        required_fields = {"id", "name", "email", "phone"}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise TypeError(f"Missing required fields: {missing_fields}")

        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )


@dataclass
class Company:
    """Company information from HubSpot."""

    id: str
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    phone: Optional[str] = None
    associated: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Company":
        """Create Company from dictionary."""
        required_fields = {"id", "name"}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise TypeError(f"Missing required fields: {missing_fields}")

        return cls(
            id=data["id"],
            name=data["name"],
            domain=data.get("domain"),
            industry=data.get("industry"),
            phone=data.get("phone"),
            associated=data.get("associated", False),
        )
