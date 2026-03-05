# Imports
import os
from flask import Flask
from .routes import EmployeeRoutes
from .extensions import db, migrate, bcrypt


def create_app():
    # Entry point
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # bind app
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    EmployeeRoutes(app, db, bcrypt)

    return app
