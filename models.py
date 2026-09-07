from datetime import datetime, timezone

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    image_file = db.Column(
        db.String(100),
        nullable=False,
        default="default.svg"
    )

    jobs = db.relationship(
        "Job",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    short_description = db.Column(
        db.String(250),
        nullable=False
    )

    full_description = db.Column(
        db.Text,
        nullable=False
    )

    company = db.Column(
        db.String(150),
        nullable=False
    )

    salary = db.Column(
        db.String(50),
        nullable=False
    )

    location = db.Column(
        db.String(120),
        nullable=False
    )

    category = db.Column(
        db.String(80),
        nullable=False
    )

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"Job('{self.title}', '{self.company}')"