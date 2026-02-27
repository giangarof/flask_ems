# Imports
import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm, DelForm, UpdateForm

# Entry point
app = Flask(__name__)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))

# configurations
app.secret_key = "secret"
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
    search = request.args.get("q")
    if search:
        employees = Employee.query.filter(Employee.name.ilike(f"%{search}%")).all()
    else:
        employees = Employee.query.all()

    return render_template("list.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():

        new_employee = Employee(
            name=form.name.data,
            about=form.about.data,
            degree=form.degree.data,
            department=form.department.data,
            salary=form.salary.data,
            employment_type=form.employment_type.data,
            hired=form.hired.data,
        )
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee created successfully!", "success")
        return redirect(url_for("list_all"))

    return render_template("add.html", form=form)


@app.route("/user/<int:id>", methods=["GET"])
def getUser(id):
    employee = Employee.query.get(id)
    return render_template("profile.html", employee=employee)


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    employee = Employee.query.get(id)
    form = UpdateForm(obj=employee)
    if form.validate_on_submit():

        employee.name = form.name.data
        employee.about = form.about.data
        employee.degree = form.degree.data
        employee.department = form.department.data
        employee.salary = form.salary.data
        employee.employment_type = form.employment_type.data
        employee.hired = form.hired.data

        db.session.commit()
        flash("Employee updated successfully!", "success")
        return redirect(url_for("list_all"))

    return render_template("update.html", form=form, employee=employee)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully!", "success")
    return redirect(url_for("list_all"))


if __name__ == "__main__":
    app.run(debug=True)
