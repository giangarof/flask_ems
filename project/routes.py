from flask import Flask, render_template, url_for, redirect, request, flash

# from . import db, bcrypt
from .forms import AddForm, DelForm, UpdateForm, AddUserForm, LoginUserForm
from .models import Employee, User
from .extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required


class EmployeeRoutes:
    def __init__(self, app, db):
        self.app = app
        self.register_routes()
        self.db = db
        self.bcrypt = bcrypt

    # Routes
    def register_routes(self):
        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("home.html")

        @self.app.route("/list")
        def list_all():
            employees = Employee.query.all()
            search = request.args.get("q")
            if search:
                employees = Employee.query.filter(
                    Employee.name.ilike(f"%{search}%")
                ).all()
            else:
                employees = Employee.query.all()

            return render_template("list.html", employees=employees)

        @self.app.route("/add", methods=["GET", "POST"])
        def add():
            form = AddForm()

            if form.validate_on_submit():

                new_employee = Employee(
                    name=form.name.data,
                    # password_hashed=bcrypt.generate_password_hash(form.password.data),
                    # email=form.email.data,
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

        @self.app.route("/user/<int:id>", methods=["GET"])
        def getUser(id):
            employee = Employee.query.get(id)
            return render_template("profile.html", employee=employee)

        @self.app.route("/update/<int:id>", methods=["GET", "POST"])
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

        @self.app.route("/delete/<int:id>", methods=["GET", "POST"])
        def delete(id):
            employee = Employee.query.get(id)
            db.session.delete(employee)
            db.session.commit()
            flash("Employee deleted successfully!", "success")
            return redirect(url_for("list_all"))


class UserRoutes:

    def __init__(self, app, db, bcrypt):
        self.app = app
        self.user_routes()
        self.db = db
        self.bcrypt = bcrypt

    def user_routes(self):

        @self.app.route("/login", methods=["GET", "POST"])
        def login():
            form = LoginUserForm()

            if form.validate_on_submit():
                # get the email first
                user = User.query.filter_by(email=form.email.data).first()
                # check the password
                if user is not None and user.check_password(form.password.data):
                    login_user(user)
                    flash("Welcome back!", "success")
                    return redirect(
                        url_for(
                            "profile",
                        )
                    )
                else:
                    flash("wrong credentials", "danger")

            return render_template("user/login.html", form=form)

        @self.app.route("/logout", methods=["GET", "POST"])
        def logout():
            pass

        @self.app.route("/signup", methods=["GET", "POST"])
        def signup():
            form = AddUserForm()
            if form.validate_on_submit():
                new_user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                )
                db.session.add(new_user)
                db.session.commit()
                flash(
                    "Thanks for creating an account with us! Please, login", "success"
                )
                return redirect(url_for("login"))
            return render_template("user/signup.html", form=form)

        @self.app.route("/profile", methods=["GET"])
        def profile():
            return render_template("user/profile.html")
