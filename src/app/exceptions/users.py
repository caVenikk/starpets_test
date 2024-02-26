from app.exceptions.base import AppException, NotFoundError


# Class that represents a user not found error
class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")


# Class that represents a username is already taken error
class UsernameTakenError(AppException):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username '{username}' is already taken")
