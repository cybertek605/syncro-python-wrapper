class SyncroError(Exception):
    """Base class for all SyncroMSP API exceptions."""
    pass

class SyncroAuthError(SyncroError):
    """Raised when authentication fails (401 Unauthorized)."""
    pass

class SyncroPermissionError(SyncroError):
    """Raised when the API token lacks permissions for an action (403 Forbidden)."""
    pass

class SyncroNotFoundError(SyncroError):
    """Raised when a requested resource is not found (404 Not Found)."""
    pass

class SyncroRateLimitError(SyncroError):
    """Raised when the API rate limit is exceeded (429 Too Many Requests)."""
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after

class SyncroServerError(SyncroError):
    """Raised when the Syncro server returns a 5xx error."""
    pass

class SyncroValidationError(SyncroError):
    """Raised when the API returns a 422 validation error."""
    pass
