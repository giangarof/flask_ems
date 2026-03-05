from .extensions import db


# Models
class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    # personal information
    name = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text)
    degree = db.Column(db.Text)
    # email = db.Column(db.Text)
    # password = db.Column(db.Text)
    # Company information
    salary = db.Column(db.Integer)
    hired = db.Column(db.Date)
    employment_type = db.Column(db.Text)
    department = db.Column(db.Text, nullable=False)
