from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize SQLAlchemy
db = SQLAlchemy()

# Starts Flask migrate
migrate = Migrate()
bcrypt = Bcrypt()
