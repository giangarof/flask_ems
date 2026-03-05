from .extensions import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text)
    degree = db.Column(db.Text)
    salary = db.Column(db.Integer)
    hired = db.Column(db.Date)
    employment_type = db.Column(db.Text)
    department = db.Column(db.Text, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    role = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    password_hashed = db.Column(db.Text)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=True)
    employee = db.relationship("Employee", backref="user", uselist=False)

    # Getter
    @property
    def password(self):
        raise AttributeError("Setter password")

    # Setter
    @password.setter
    def password(self, plaintext):
        self.password_hashed = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hashed, plaintext)
