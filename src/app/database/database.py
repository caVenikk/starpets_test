import aiosqlite

from app.database.repository.users_repository import UserRepository
from config import load_config

config = load_config()


# Database class that contains the connection to the database and the repositories
class Database:
    def __init__(self) -> None:
        self.connection = aiosqlite.connect(config.database.filename)
        self.users = UserRepository(self.connection)

    def __call__(self) -> "Database":
        return self
