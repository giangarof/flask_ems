from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    IntegerField,
    SubmitField,
    SelectField,
    DateField,
    PasswordField,
    EmailField,
)
from wtforms.validators import DataRequired, Email, EqualTo

# EMPLOYEE

class CreateEmployeeForm(FlaskForm):
    name = StringField("Enter your name")
    email = EmailField("Your email")
    degree = SelectField(
        "Highest Degree",
        choices=[
            ("AA", "AA"),
            ("AS", "AS"),
            ("BA", "BA"),
            ("BS", "BS"),
            ("MS", "MS"),
            ("PHD", "PHD"),
            # ("Active", "Active"),
        ],
    )
    status = SelectField(
        "Status",
        choices=[
            ("Unassigned", "Unassigned"),
            # ("Active", "Active"),
        ],
    )
    submit = SubmitField("Create Employee")


class DelEmployeeForm(FlaskForm):
    id = IntegerField("ID user number to remove: ")
    submit = SubmitField("Remove User")


class AssignEmployeeForm(FlaskForm):
    salary = IntegerField("Salary compesation")
    hired = DateField("Hired date")
    role = StringField("Employee role")
    company_id = SelectField("Company", coerce=int)
    employment_type = SelectField(
        "Employment Type",
        choices=[
            ("Full-Time", "Full-Time"),
            ("Part-Time", "Part-Time"),
            ("Volunteer", "Volunteer"),
            ("Seasonal", "Seasonal"),
            ("Apprenticeship", "Apprenticeship"),
        ],
    )
    department = SelectField("Department", coerce=int)
    submit = SubmitField("Assign Employee")


class UpdateUnassignedFom(FlaskForm):
    name = StringField("Update name")
    email = EmailField("Update Email")
    degree = SelectField(
        "Highest Degree",
        choices=[
            ("High School","High School"),
            ("AA", "AA"),
            ("AS", "AS"),
            ("BA", "BA"),
            ("BS", "BS"),
            ("MS", "MS"),
            ("PHD", "PHD"),
        ],
    )
    submit = SubmitField("Update unassigned employee")


class UpdateAssignedFom(FlaskForm):
    salary = IntegerField("Salary compesation")
    hired = DateField("Hired date")
    role = StringField("Employee role")
    # company_id = SelectField("Company", coerce=int)
    employment_type = SelectField(
        "Employment Type",
        choices=[
            ("Full-Time", "Full-Time"),
            ("Part-Time", "Part-Time"),
            ("Volunteer", "Volunteer"),
            ("Seasonal", "Seasonal"),
            ("Apprenticeship", "Apprenticeship"),
        ],
    )
    department = SelectField("Department", coerce=int)
    submit = SubmitField("Update Employee")


# USER

class SignupUserForm(FlaskForm):
    name = StringField("Enter your name", validators=[DataRequired()])
    password = PasswordField("Set your password", validators=[DataRequired()])
    email = EmailField("Your email", validators=[DataRequired(), Email()])

    submit = SubmitField("Create User")


class LoginUserForm(FlaskForm):
    password = PasswordField("Your password", validators=[DataRequired()])
    email = EmailField("Your email", validators=[DataRequired(), Email()])
    submit = SubmitField("LogIn User")


# COMPANY
class CreateCompanyForm(FlaskForm):
    name = StringField("New company name", validators=[DataRequired()])
    about = TextAreaField("What is the company about?", validators=[DataRequired()])
    submit = SubmitField("Create Company")


class UpdateCompanyForm(FlaskForm):
    name = StringField("Update company name", validators=[DataRequired()])
    about = TextAreaField("What is the company about?", validators=[DataRequired()])
    submit = SubmitField("Update Company")


# DEPARTMENT

class AddDepartmentForm(FlaskForm):
    name = StringField('Department name to add')
    submit = SubmitField("Add Department to your Company")