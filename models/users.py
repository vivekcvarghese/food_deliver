from db import db
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)

    __table_args__ = (
        CheckConstraint(role.in_(['admin', 'agent', 'customer'])),
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)