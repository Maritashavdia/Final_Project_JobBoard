from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
)

from models import User


class RegistrationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField("Create Account")

    def validate_name(self, name):
        existing_user = User.query.filter_by(
            name=name.data.strip()
        ).first()

        if existing_user:
            raise ValidationError(
                "This name is already in use."
            )

    def validate_email(self, email):
        existing_user = User.query.filter_by(
            email=email.data.strip().lower()
        ).first()

        if existing_user:
            raise ValidationError(
                "This email is already registered."
            )


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField("Remember me")

    submit = SubmitField("Log In")


class UpdateProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    picture = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Only JPG, JPEG and PNG images are allowed."
            )
        ]
    )

    submit = SubmitField("Save Changes")

    def __init__(
        self,
        original_name=None,
        original_email=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_email = original_email

    def validate_name(self, name):
        cleaned_name = name.data.strip()

        if (
            self.original_name
            and cleaned_name != self.original_name
        ):
            existing_user = User.query.filter_by(
                name=cleaned_name
            ).first()

            if existing_user:
                raise ValidationError(
                    "This name is already in use."
                )

    def validate_email(self, email):
        cleaned_email = email.data.strip().lower()

        if (
            self.original_email
            and cleaned_email != self.original_email
        ):
            existing_user = User.query.filter_by(
                email=cleaned_email
            ).first()

            if existing_user:
                raise ValidationError(
                    "This email is already registered."
                )


class JobForm(FlaskForm):
    title = StringField(
        "Job Title",
        validators=[
            DataRequired(),
            Length(min=2, max=150)
        ]
    )

    company = StringField(
        "Company",
        validators=[
            DataRequired(),
            Length(min=2, max=150)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            DataRequired(),
            Length(min=2, max=120)
        ]
    )

    salary = StringField(
        "Salary",
        validators=[
            DataRequired(),
            Length(min=2, max=50)
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Technology", "Technology"),
            ("Design", "Design"),
            ("Marketing", "Marketing"),
            ("Finance", "Finance"),
            ("Sales", "Sales"),
            ("Customer Service", "Customer Service"),
            ("Human Resources", "Human Resources"),
            ("Other", "Other")
        ],
        validators=[
            DataRequired()
        ]
    )

    short_description = TextAreaField(
        "Short Description",
        validators=[
            DataRequired(),
            Length(min=10, max=250)
        ]
    )

    full_description = TextAreaField(
        "Full Description",
        validators=[
            DataRequired(),
            Length(min=20)
        ]
    )

    submit = SubmitField("Save Job")

class DeleteJobForm(FlaskForm):
    submit = SubmitField("Delete Job")