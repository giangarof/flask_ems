from flask import Flask, abort, render_template, url_for, redirect, request, flash

# from . import db, bcrypt
from .forms import (
    CreateEmployeeForm,
    DelEmployeeForm,
    SignupUserForm,
    LoginUserForm,
    CreateCompanyForm,
    UpdateCompanyForm,
    AssignEmployeeForm,
    UpdateUnassignedFom,
    UpdateAssignedFom,
    AddDepartmentForm,
)
from .models import Employee, User, Company, Department
from .extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user


class BaseRoutes:

    def __init__(self, app):
        self.app = app
        self.base_routes()

    def base_routes(self):

        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("home.html")


class EmployeeRoutes:
    def __init__(self, app, db):
        self.app = app
        self.employee_routes()
        self.db = db
        self.bcrypt = bcrypt

    # Routes
    def employee_routes(self):

        # FIRST PART
        # UNASSIGNED EMPLOYEE SECTION

        # CREATE EMPLOYEE
        # UNASSIGNED BY DEFAULT
        @self.app.route("/add", methods=["GET", "POST"])
        def add():
            form = CreateEmployeeForm()

            if form.validate_on_submit():

                new_employee = Employee(
                    name=form.name.data,
                    email=form.email.data,
                    degree=form.degree.data,
                    status=form.status.data,
                    created_by=current_user.id,
                )
                db.session.add(new_employee)
                db.session.commit()
                flash("Employee created successfully!", "success")
                return redirect(url_for("list_all_employees"))

            return render_template("employee/createEmployee.html", form=form)

        # UPDATE EMPLOYEE UNASSIGNED
        @self.app.route("/update_unassiged/<int:id>", methods=["GET", "POST"])
        def updateUnassigned(id):
            employee = Employee.query.get(id)
            form = UpdateUnassignedFom(obj=employee)
            if form.validate_on_submit():

                employee.name = form.name.data
                employee.email = form.email.data
                employee.degree = form.degree.data

                db.session.commit()
                flash("Employee updated successfully!", "success")
                return redirect(url_for("profile"))

            return render_template(
                "employee/updateUnassigned.html", form=form, employee=employee
            )

        # LIST ALL UNASSIGNED
        # FILTER BY CREATED_BY
        @self.app.route("/list_employees")
        def list_all_employees():
            employees = Employee.query.filter_by(created_by=current_user.id).all()

            return render_template("employee/listAllEmployee.html", employees=employees)

        # DELETE EMPLOYEE FROM DB
        @self.app.route("/delete/<int:id>", methods=["GET", "POST"])
        def delete(id):
            employee = Employee.query.get(id)
            if employee.created_by != current_user.id:
                abort(403)
            db.session.delete(employee)
            db.session.commit()
            flash("Employee deleted successfully!", "success")
            return redirect(url_for("list_all_employees"))

        # SECONG PART
        # ASSIGNED EMPLOYEE

        # ASIGN EMPLOYEE TO A COMPANY
        # CHANGE STATUS FROM UNASIGNED TO ACTIVE
        @self.app.route("/assign/<int:id>", methods=["GET", "POST"])
        def assignEmployee(id):
            form = AssignEmployeeForm()
            # get the employee id
            employee = Employee.query.get(id)

            # query only the companies that the user has
            companies = Company.query.filter_by(owner_id=current_user.id).all()

            # populate select field dynamically
            form.company_id.choices = [(c.id, c.name) for c in companies]

            # form to assign
            if form.validate_on_submit():
                employee.salary = form.salary.data
                employee.hired = form.hired.data
                employee.role = form.role.data
                employee.employment_type = form.employment_type.data
                employee.department = form.department.data
                employee.company_id = form.company_id.data
                employee.status = "Active"

                db.session.commit()
                flash("Employee assigned successfully!", "success")
                return redirect(url_for("profile"))

            return render_template(
                "employee/assignToACompany.html", form=form, employee=employee
            )

        # UPDATE ASSIGNED EMPLOYEE
        @self.app.route("/update_assiged/<int:id>", methods=["GET", "POST"])
        def updateAssigned(id):
            employee = Employee.query.get(id)
            form = UpdateAssignedFom(obj=employee)
            if form.validate_on_submit():

                employee.salary = form.salary.data
                employee.hired = form.hired.data
                employee.role = form.role.data
                employee.employment_type = form.employment_type.data
                employee.department = form.department.data

                db.session.commit()
                flash("Employee updated successfully!", "success")
                return redirect(url_for("profile"))

            return render_template(
                "employee/updateAssigned.html", form=form, employee=employee
            )

        # REMOVE FROM ACTIVE TO UNASSIGNED
        @self.app.route("/remove/<int:id>", methods=["GET", "POST"])
        def unassignEmployee(id):
            employee = Employee.query.get(id)
            if employee.created_by == current_user.id:
                employee.status = "Unassigned"

            db.session.commit()
            flash("Employee removed from the company", "success")
            return redirect(url_for("profile"))


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
        @login_required
        def logout():
            logout_user()
            flash("You have been logeed out.", "success")
            return redirect(url_for("login"))

        @self.app.route("/signup", methods=["GET", "POST"])
        def signup():
            form = SignupUserForm()
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
        @login_required
        def profile():
            return render_template("user/profile.html")


class CompanyRoutes:

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.company_routes()

    def company_routes(self):

        @self.app.route("/companies", methods=["GET"])
        @login_required
        def companies():
            companies = Company.query.filter_by(owner_id=current_user.id).all()
            return render_template("company/companies.html", companies=companies)

        @self.app.route("/add_company", methods=["GET", "POST"])
        @login_required
        def createCompany():
            form = CreateCompanyForm()
            if form.validate_on_submit():
                new_company = Company(
                    name=form.name.data, about=form.about.data, owner_id=current_user.id
                )
                db.session.add(new_company)
                db.session.commit()

                flash("Company created successfully", "success")
                return redirect(url_for("profile"))
            return render_template("company/addCompany.html", form=form)

        @self.app.route("/update_company/<int:id>", methods=["GET", "POST"])
        @login_required
        def updateCompany(id):
            company = Company.query.get(id)
            form = UpdateCompanyForm(obj=company)
            if form.validate_on_submit():
                company.name = form.name.data
                company.about = form.about.data

                db.session.commit()
                flash("company updated successfully!", "success")
                return redirect(url_for("companies"))

            return render_template(
                "company/updateCompany.html", form=form, company=company
            )

        @self.app.route("/delete_company/<int:id>", methods=["GET", "POST"])
        @login_required
        def deleteCompany(id):
            company = Company.query.get(id)
            if company.owner_id != current_user.id:
                abort(403)
            db.session.delete(company)
            db.session.commit()

            flash("Company deleted successfully", "success")
            return redirect(url_for("companies"))

        @self.app.route("/company_employees/<int:id>", methods=["GET"])
        def list_company_employees(id):
            employees = Employee.query.filter_by(company_id=id, status="Active").all()
            return render_template("company/companyEmployees.html", employees=employees)

        @self.app.route("/departments/<int:id>", methods=["GET", "POST"])
        def departments(id):
            form = AddDepartmentForm()
            company = Company.query.get(id)
            departments = Department.query.filter_by(company_id=company.id).all()

            if form.validate_on_submit():
                new_department = Department(name=form.name.data, company_id=company.id)
                db.session.add(new_department)
                db.session.commit()

                flash("Department created successfully", "success")
                return redirect(request.url)
            return render_template(
                "company/departments.html",
                departments=departments,
                company=company,
                form=form,
            )

        @self.app.route(
            "/remove_department/<int:company_id>/<int:department_id>",
            methods=["POST"],
        )
        @login_required
        def removeDepartment(company_id, department_id):
            company = Company.query.get_or_404(company_id)
            department = Department.query.get_or_404(department_id)
            userID = current_user.id
            companyOwner = company.owner_id

            if userID != companyOwner and department.company_id != company.id:
                abort(403)

            db.session.delete(department)
            db.session.commit()

            flash("Department deleted successfully", "success")
            return redirect(url_for('departments',id=company_id))
