from app.exceptions.base import NotFoundError


# Class that represents an error when a city is not found
class CityNotFoundError(NotFoundError):
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"City '{city}' not found")
