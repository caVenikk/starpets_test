from dataclasses import dataclass


# User create request schema
@dataclass
class UserCreateRequest:
    username: str
    balance: float


# User update request schema
@dataclass
class UserUpdateRequest:
    username: str | None = None
    balance: float | None = None
