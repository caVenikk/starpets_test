from typing import Any, Literal

from app.request_schemas import UserCreateRequest, UserUpdateRequest

"""
This file contains validators for presented request data.
These validators are used to check if the request data is valid.
"""


# Validator for user creation request
class UserCreateRequestValidator:
    def __init__(self, user_create_request: UserCreateRequest):
        self.user_create_request = user_create_request
        self._errors: dict[Literal["errors"], list[str]] = {"errors": []}

    async def validate(self) -> dict[Literal["errors"], list[str]] | None:
        self.validate_username()
        self.validate_balance()

        if self._errors["errors"]:
            return self._errors
        return None

    def validate_username(self) -> None:
        if self.user_create_request.username is None:
            self._errors["errors"].append("Username can't be empty")
            return

        if not isinstance(self.user_create_request.username, str):
            self._errors["errors"].append("Username must be a string")
            return

        if len(self.user_create_request.username) < 3:
            self._errors["errors"].append("Username must be at least 3 characters long")

    def validate_balance(self) -> None:
        if self.user_create_request.balance is None:
            self._errors["errors"].append("Balance can't be empty")
            return

        if not isinstance(self.user_create_request.balance, float) and not isinstance(
            self.user_create_request.balance, int
        ):
            self._errors["errors"].append("Balance must be a number")
            return

        if self.user_create_request.balance < 0:
            self._errors["errors"].append("Balance can't be negative")


# Validator for user balance update
class UserBalanceUpdateValidator:
    def __init__(self, balance: Any):
        self.balance = balance
        self._errors: dict[Literal["errors"], list[str]] = {"errors": []}

    async def validate(self) -> dict[Literal["errors"], list[str]] | None:
        self.validate_balance()

        if self._errors["errors"]:
            return self._errors
        return None

    def validate_balance(self) -> None:
        if self.balance is None:
            self._errors["errors"].append("Balance can't be empty")
            return

        if not isinstance(self.balance, int) and not isinstance(self.balance, float):
            self._errors["errors"].append("Balance must be a number")
            return

        if self.balance < 0:
            self._errors["errors"].append("Balance can't be negative")


# Validator for city
class CityValidator:
    def __init__(self, city: Any):
        self.city = city
        self._errors: dict[Literal["errors"], list[str]] = {"errors": []}

    async def validate(self) -> dict[Literal["errors"], list[str]] | None:
        self.validate_city()

        if self._errors["errors"]:
            return self._errors
        return None

    def validate_city(self) -> None:
        if self.city is None:
            self._errors["errors"].append("City can't be empty")
            return

        if not isinstance(self.city, str):
            self._errors["errors"].append("City must be a string")
            return

        if len(self.city) < 2:
            self._errors["errors"].append("City must be at least 2 characters long")


# Validator for user update request
class UserUpdateRequestValidator:
    def __init__(self, user_update_request: UserUpdateRequest):
        self.user_update_request = user_update_request
        self._errors: dict[Literal["errors"], list[str]] = {"errors": []}

    async def validate(self) -> dict[Literal["errors"], list[str]] | None:
        if self.user_update_request.username is not None:
            self.validate_username()

        if self.user_update_request.balance is not None:
            self.validate_balance()

        if self._errors["errors"]:
            return self._errors
        return None

    def validate_username(self) -> None:
        if not isinstance(self.user_update_request.username, str):
            self._errors["errors"].append("Username must be a string")
            return

        if len(self.user_update_request.username) < 3:
            self._errors["errors"].append("Username must be at least 3 characters long")

    def validate_balance(self) -> None:
        if (
            self.user_update_request.balance
            and not isinstance(self.user_update_request.balance, float)
            and not isinstance(self.user_update_request.balance, int)
        ):
            self._errors["errors"].append("Balance must be a number")
            return

        if self.user_update_request.balance is not None and self.user_update_request.balance < 0:
            self._errors["errors"].append("Balance can't be negative")
