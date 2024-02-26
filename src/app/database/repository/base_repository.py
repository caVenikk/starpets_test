from aiosqlite import Connection


# Base repository class that contains the connection to the database
class BaseRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def commit(self) -> None:
        await self._connection.commit()
