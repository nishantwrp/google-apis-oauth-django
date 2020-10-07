"""Custom exceptions that are used in this package."""

class InvalidLoginException(Exception):
    """Raised when an unauthenticated request is made to the redirect uri."""
