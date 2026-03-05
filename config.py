import os


class Config:
    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))

    # app.secret_key = "secret"
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
