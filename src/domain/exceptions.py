class HubSpotException(Exception):
    """Base exception for HubSpot-related errors."""

    pass


class HubSpotAuthenticationError(HubSpotException):
    """Exception raised when there are authentication issues with HubSpot."""

    pass


class HubSpotOperationError(HubSpotException):
    """Exception raised when HubSpot operations fail."""

    pass
