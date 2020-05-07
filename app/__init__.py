from flask import Flask

app = Flask(__name__)

# Import the routes module which as side-effect declares the Flask routes.
from app import routes

_ = routes
