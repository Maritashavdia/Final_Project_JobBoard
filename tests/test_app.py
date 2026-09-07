import os

import pytest


os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app
from models import Job, User, db


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def create_user(
    name,
    email,
    password="password123"
):
    user = User(
        name=name,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


def test_home_page_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"JobBoard" in response.data
    assert b"Latest opportunities" in response.data


def test_user_can_log_in(client):
    create_user(
        name="Test User",
        email="test@example.com"
    )

    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123",
            "remember": False
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome back!" in response.data
    assert b"Log Out" in response.data


def test_user_cannot_modify_another_users_job(client):
    owner = create_user(
        name="Job Owner",
        email="owner@example.com"
    )

    other_user = create_user(
        name="Other User",
        email="other@example.com"
    )

    job = Job(
        title="Data Analyst",
        short_description=(
            "Analyze business data and prepare useful reports."
        ),
        full_description=(
            "The Data Analyst will prepare reports, "
            "dashboards and business insights."
        ),
        company="GeoData Analytics",
        salary="2,500–3,500 GEL",
        location="Tbilisi, Georgia",
        category="Data & Analytics",
        author=owner
    )

    db.session.add(job)
    db.session.commit()

    job_id = job.id

    login_response = client.post(
        "/login",
        data={
            "email": other_user.email,
            "password": "password123",
            "remember": False
        },
        follow_redirects=True
    )

    assert login_response.status_code == 200

    edit_response = client.get(
        f"/job/{job_id}/edit"
    )

    assert edit_response.status_code == 403

    delete_response = client.post(
        f"/job/{job_id}/delete"
    )

    assert delete_response.status_code == 403

    existing_job = db.session.get(
        Job,
        job_id
    )

    assert existing_job is not None