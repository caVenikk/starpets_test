from flask import Flask

app = Flask(__name__)

# Reading routes
from app import users  # noqa
