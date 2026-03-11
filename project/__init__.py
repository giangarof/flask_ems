# Imports
import os
from flask import Flask
from .routes import EmployeeRoutes, UserRoutes, CompanyRoutes
from .extensions import db, migrate, bcrypt, login_manager
from .models import User


def create_app():
    # Entry point
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # bind app
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    EmployeeRoutes(app, db)
    UserRoutes(app, db, bcrypt)
    CompanyRoutes(app, db)

    return app
