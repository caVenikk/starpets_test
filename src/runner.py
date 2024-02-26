from app import app


@app.route("/")
async def root() -> str:
    return "Test project for starpets.gg"


if __name__ == "__main__":
    app.run()
