# Imports
import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm, DelForm

# Entry point
app = Flask(__name__)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))

# configurations
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Starts Flask migrate
Migrate(app, db)

# Note before starting
# flask db init	                    Start migration system
# flask db migrate -m "message"	    Generate change script
# flask db upgrade	                Apply changes to database
# Run: flask db migrate each time you do modify the models


# Models
class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text)
    degree = db.Column(db.Text)
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.id"), nullable=False
    )
    # department = db.relationship("Department")


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.Text)

    employee = db.relationship("Employee", backref="department", lazy=True)


# Routes


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/list")
def list_all():
    employees = Employee.query.all()
    return render_template("list.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")


@app.route("/update", methods=["GET", "POST"])
def update():
    pass


@app.route("/delete", methods=["GET", "POST"])
def delete():
    pass


if __name__ == "__main__":
    app.run(debug=True)
