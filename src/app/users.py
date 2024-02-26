from flask import request

from app import app
from app.database.database import Database
from app.exceptions.users import UsernameTakenError, UserNotFoundError
from app.exceptions.weather import CityNotFoundError
from app.request_schemas import UserCreateRequest, UserUpdateRequest
from app.services.weather import fetch_weather
from app.validators.users import (CityValidator, UserBalanceUpdateValidator,
                                  UserCreateRequestValidator,
                                  UserUpdateRequestValidator)


@app.route("/users", methods=["GET"])
async def get_all_users() -> list[dict]:
    limit = request.args.get("limit")
    offset = request.args.get("offset")

    database = Database()
    users = await database.users.all(limit, offset)

    return [user.to_dict() for user in users]


@app.route("/users", methods=["POST"])
async def create_user() -> dict | tuple[dict, int]:
    data = request.get_json()
    try:
        user_create_request = UserCreateRequest(**data)
    except TypeError:
        return {"error": "Invalid request body"}, 400

    validator = UserCreateRequestValidator(user_create_request)
    errors = await validator.validate()
    if errors:
        return errors, 400

    database = Database()
    try:
        user = await database.users.create(user_create_request)
    except UsernameTakenError as e:
        return {"error": str(e)}, 400

    return user.to_dict(), 201


@app.route("/users/<int:user_id>", methods=["GET"])
async def get_user(user_id: int) -> dict | tuple[dict, int]:
    database = Database()
    if (user := await database.users.get(user_id)) is None:
        return {"error": "User not found"}, 404

    return user.to_dict()


@app.route("/users/<int:user_id>", methods=["PUT"])
async def update_user(user_id: int) -> dict | tuple[dict, int]:
    database = Database()
    if (user := await database.users.get(user_id)) is None:
        return {"error": "User not found"}, 404

    data = request.get_json()
    try:
        user_update_request = UserUpdateRequest(**data)
    except TypeError:
        return {"error": "Invalid request body"}, 400
    validator = UserUpdateRequestValidator(user_update_request)
    errors = await validator.validate()

    if errors:
        return errors, 400

    # New connection
    database = Database()
    try:
        new_user = await database.users.update(user, user_update_request)
    except UserNotFoundError as e:
        return {"error": str(e)}, 404
    except UsernameTakenError as e:
        return {"error": str(e)}, 400

    return new_user.to_dict()


@app.route("/users/<int:user_id>", methods=["DELETE"])
async def delete_user(user_id: int) -> dict | tuple[dict, int]:
    database = Database()
    if (user := await database.users.get(user_id)) is None:
        return {"error": "User not found"}, 404

    # New connection
    database = Database()
    await database.users.delete(user)

    return {"message": "User deleted"}


@app.route("/users/<int:user_id>/update_balance", methods=["POST"])
async def update_user_balance(user_id: int) -> dict | tuple[dict, int]:
    database = Database()
    if (user := await database.users.get(user_id)) is None:
        return {"error": "User not found"}, 404

    balance = request.get_json().get("balance", None)
    validator = UserBalanceUpdateValidator(balance)
    errors = await validator.validate()

    if errors:
        return errors, 400

    # New connection
    database = Database()
    new_user = await database.users.update_balance(user, balance)

    return new_user.to_dict()


@app.route("/users/<int:user_id>/city", methods=["POST"])
async def update_user_balance_by_city(user_id: int) -> dict | tuple[dict, int]:
    database = Database()
    if (user := await database.users.get(user_id)) is None:
        return {"error": "User not found"}, 404

    city = request.get_json().get("city", None)
    validator = CityValidator(city)
    errors = await validator.validate()

    if errors:
        return errors, 400

    try:
        weather = fetch_weather(city)
    except CityNotFoundError as e:
        return {"error": str(e)}, 404

    if (temperature := weather.get("main", {}).get("temp", None)) is None:
        return {"error": "Unable to determine temperature"}, 500

    # New connection
    database = Database()
    new_user = await database.users.add_balance(user, temperature)

    return new_user.to_dict()
