import os

from dotenv import load_dotenv


load_dotenv()


database_url = os.environ.get(
    "DATABASE_URL",
    "sqlite:///jobboard.db"
)


if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )

elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "jobboard-development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "static",
        "profile_pics"
    )

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024