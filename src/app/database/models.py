from dataclasses import dataclass


# Dataclass for User model
@dataclass
class User:
    id: int
    username: str
    balance: float

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "balance": self.balance,
        }
