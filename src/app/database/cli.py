import asyncio
import sys
from random import randint

import aiosqlite

from config import load_config

config = load_config()

"""
This script is used to create, drop and fill the database with random data.
"""


# Create table users
async def create_database() -> None:
    try:
        async with aiosqlite.connect(config.database.filename) as db:
            cursor = await db.cursor()
            await cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    balance FLOAT NOT NULL
                                )"""
            )
            print("Database created successfully")
    except aiosqlite.Error as e:
        print("Error creating database:", e)


# Drop table users
async def drop_database() -> None:
    try:
        async with aiosqlite.connect(config.database.filename) as db:
            cursor = await db.cursor()
            await cursor.execute("""DROP TABLE IF EXISTS users""")

            print("Database dropped successfully")
    except aiosqlite.Error as e:
        print("Error dropping database:", e)


# Fill table users with random data
async def fill_database() -> None:
    try:
        async with aiosqlite.connect(config.database.filename) as db:
            cursor = await db.cursor()

            for i in range(5):
                await cursor.execute(
                    f"""
                    INSERT INTO users (username, balance)
                    VALUES
                    ('user{i + 1}', {randint(5000, 15000)})
                    """
                )

            await db.commit()

            print("Database filled successfully")
    except aiosqlite.Error as e:
        print("Error filling database:", e)


# Main function handling the action
async def main(_action: str) -> None:
    match _action:
        case "create":
            await create_database()
        case "drop":
            await drop_database()
        case "fill":
            await fill_database()
        case _:
            print("Invalid action. Use 'create', 'drop' or 'fill'")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli.py <create/drop/fill>")
        sys.exit(1)

    action = sys.argv[1].lower()

    asyncio.run(main(action))
