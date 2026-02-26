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
    # personal information
    name = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text)
    degree = db.Column(db.Text)
    # Company information
    salary = db.Column(db.Integer)
    hired = db.Column(db.Date)
    employment_type = db.Column(db.Text)
    department = db.Column(db.Text, nullable=False)


# Routes
@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/list")
def list_all():
    employees = Employee.query.all()
    print(type(employees))
    return render_template("list.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        about = form.about.data
        degree = form.degree.data
        department = form.department.data
        salary = form.salary.data
        employment_type = form.employment_type.data
        hired = form.hired.data

        new_employee = Employee(
            name, about, degree, department, salary, employment_type, hired
        )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for("list_all"))

    return render_template("add.html", form=form)


@app.route("/user/<int:id>", methods=["GET"])
def getUser(id):
    employee = Employee.query.get(id)
    return render_template("profile.html", employee=employee)


@app.route("/update", methods=["GET", "POST"])
def update():
    pass


@app.route("/delete", methods=["GET", "POST"])
def delete():
    pass


if __name__ == "__main__":
    app.run(debug=True)
