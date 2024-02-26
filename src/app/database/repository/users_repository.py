from sqlite3 import IntegrityError

from aiosqlite import Connection

from app.exceptions.users import UsernameTakenError
from app.request_schemas import UserCreateRequest, UserUpdateRequest
from src.app.database.models import User
from src.app.database.repository.base_repository import BaseRepository


# User repository class that handles all the database operations related to users
class UserRepository(BaseRepository):
    # Initialize the repository with a connection to the database
    def __init__(self, connection: Connection):
        super().__init__(connection)

    # Get a user from the database by their id using a connection from another method
    @staticmethod
    async def _get(connection: Connection, user_id: int) -> User | None:
        cursor = await connection.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        if user is None:
            return None
        return User(*user)

    # Get the last user from the database using a connection from another method
    @staticmethod
    async def _last(connection: Connection) -> User | None:
        cursor = await connection.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
        user = await cursor.fetchone()
        return User(*user) if user else None

    # Build an update query for a user using their current data and the new data
    @staticmethod
    def _build_update_query(db_user: User, update_data: UserUpdateRequest) -> str | None:
        if update_data.balance is not None:
            balance = update_data.balance if update_data.balance >= 0 else 0
        else:
            balance = None

        query = "UPDATE users SET "

        if update_data.username != db_user.username and update_data.username is not None:
            query += f"username = '{update_data.username}'"
        if balance != db_user.balance and balance is not None:
            if "username" in query:
                query += ", "
            query += f"balance = {balance}"

        if query == "UPDATE users SET ":
            return None

        query += f" WHERE id = {db_user.id}"
        return query

    # Create a new user in the database
    async def create(self, user: UserCreateRequest) -> User | None:
        async with self._connection as conn:
            query = "INSERT INTO users (username, balance) VALUES (?, ?);"

            # Handle the case when the username is already taken
            try:
                await conn.execute(query, (user.username, user.balance))
            except IntegrityError:
                raise UsernameTakenError(user.username)
            await self.commit()

            return await self._last(conn)

    # Get all the users from the database with optional limit and offset
    async def all(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        async with self._connection as conn:
            query = "SELECT * FROM users ORDER BY id DESC"
            if limit is not None:
                query += f" LIMIT {limit}"
            if offset is not None:
                query += f" OFFSET {offset}"

            cursor = await conn.execute(query)
            users = await cursor.fetchall()
            return [User(*user) for user in users]

    # Get a user from the database by their id
    async def get(self, user_id: int) -> User | None:
        async with self._connection as conn:
            cursor = await conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = await cursor.fetchone()
            return User(*user) if user else None

    # Update a user in the database
    async def update(self, db_user: User, update_data: UserUpdateRequest) -> User | None:
        if update_data.balance is not None:
            balance = update_data.balance if update_data.balance >= 0 else 0
        else:
            balance = None

        async with self._connection as conn:
            if not (query := self._build_update_query(db_user, update_data)):
                return db_user

            try:
                await conn.execute(query)
            except IntegrityError:
                raise UsernameTakenError(update_data.username)
            await self.commit()

            # Update the user object with the new data
            if update_data.username is not None:
                db_user.username = update_data.username
            if balance is not None:
                db_user.balance = balance

            return db_user

    # Delete a user from the database
    async def delete(self, user: User) -> User | None:
        async with self._connection as conn:
            await conn.execute("DELETE FROM users WHERE id = ?", (user.id,))
            await self.commit()

            return user

    # Update the balance of a user
    async def update_balance(self, user: User, balance: float) -> User | None:
        balance_to_set = balance if balance >= 0 else 0

        async with self._connection as conn:
            await conn.execute("UPDATE users SET balance = ? WHERE id = ?", (balance_to_set, user.id))
            await self.commit()
            user.balance = balance_to_set

            return user

    # Add to the balance of a user
    async def add_balance(self, user: User, amount: float) -> User:
        async with self._connection as conn:
            balance_to_set = user.balance + amount
            _balance = balance_to_set if balance_to_set >= 0 else 0

            await conn.execute("UPDATE users SET balance = ? WHERE id = ?", (_balance, user.id))
            await self.commit()
            user.balance = _balance

            return user
