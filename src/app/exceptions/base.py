"""
Base exceptions for the application
"""


class AppException(Exception):
    """Base App Exception"""


class NotFoundError(AppException):
    """Not found"""
