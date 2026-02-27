from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField


class AddForm(FlaskForm):
    name = StringField("Enter your name")
    about = StringField("About me")
    degree = StringField("Highest degree")
    salary = IntegerField("Salary compesation")
    hired = DateField("Hired date")
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
    department = SelectField(
        "Department",
        choices=[
            ("IT", "IT"),
            ("Help Desk", "Help Desk"),
            ("HR", "HR"),
            ("SWE", "SWE"),
            ("Data Analytics", "Data Analytics"),
            ("FrontEnd", "FrontEnd"),
            ("Backend", "Backend"),
        ],
    )
    submit = SubmitField("Add User")


class DelForm(FlaskForm):
    id = IntegerField("ID user number to remove: ")
    submit = SubmitField("Remove User")


class UpdateForm(FlaskForm):
    name = StringField("Enter your name")
    about = StringField("About me")
    degree = StringField("Highest degree")
    salary = IntegerField("Salary compesation")
    hired = DateField("Hired date")
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
    department = SelectField(
        "Department",
        choices=[
            ("IT", "IT"),
            ("Help Desk", "Help Desk"),
            ("HR", "HR"),
            ("SWE", "SWE"),
            ("Data Analytics", "Data Analytics"),
            ("FrontEnd", "FrontEnd"),
            ("Backend", "Backend"),
        ],
    )
    submit = SubmitField("Update User")
