class NotFoundError(Exception):
    """Exception raised when an error not found entity."""


class AlreadyExistsError(Exception):
    """Exception raised when entity already exists."""


class ForbiddenError(Exception):
    """Exception raised когда не хватает прав."""


class FSAPIError(Exception):
    """Ошибки апи freeswitch"""
