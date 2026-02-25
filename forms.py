from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField


class AddForm(FlaskForm):
    name = StringField("Enter your name")
    about = StringField("About me")
    degree = StringField("Highest degree")
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
    id = IntegerField("ID user number to remove: ")
    name = StringField("Enter your name")
    about = StringField("About me")
    degree = StringField("Highest degree")
    department = StringField("Enter department")
    submit = SubmitField("Update User")
