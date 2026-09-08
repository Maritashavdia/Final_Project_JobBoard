import logging
import os
import secrets

import requests
from PIL import Image
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from config import Config
from forms import (
    DeleteJobForm,
    JobForm,
    LoginForm,
    RegistrationForm,
    UpdateProfileForm
)
from models import Job, User, db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("jobboard.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def save_picture(form_picture):
    random_name = secrets.token_hex(8)

    file_extension = os.path.splitext(
        form_picture.filename
    )[1].lower()

    picture_filename = random_name + file_extension

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    picture_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        picture_filename
    )

    image = Image.open(form_picture)
    image.thumbnail((300, 300))
    image.save(picture_path)

    return picture_filename


def get_external_quote():
    default_quote = {
        "quote": "Great opportunities begin with one small step.",
        "author": "JobBoard"
    }

    try:
        response = requests.get(
            "https://dummyjson.com/quotes/random",
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

        return {
            "quote": data.get(
                "quote",
                default_quote["quote"]
            ),
            "author": data.get(
                "author",
                default_quote["author"]
            )
        }

    except requests.RequestException as error:
        logger.error(
            "External API request failed: %s",
            error
        )

        return default_quote


@app.route("/")
@app.route("/home")
def index():
    selected_category = request.args.get(
        "category",
        ""
    ).strip()

    selected_sort = request.args.get(
        "sort",
        "newest"
    ).strip()

    if selected_sort not in {"newest", "oldest"}:
        selected_sort = "newest"

    jobs_query = Job.query

    if selected_category:
        jobs_query = jobs_query.filter_by(
            category=selected_category
        )

    if selected_sort == "oldest":
        jobs_query = jobs_query.order_by(
            Job.date_posted.asc()
        )
    else:
        jobs_query = jobs_query.order_by(
            Job.date_posted.desc()
        )

    jobs = jobs_query.all()

    categories = [
        category
        for category, in (
            db.session.query(Job.category)
            .distinct()
            .order_by(Job.category)
            .all()
        )
        if category
    ]

    return render_template(
        "index.html",
        jobs=jobs,
        categories=categories,
        selected_category=selected_category,
        selected_sort=selected_sort,
        title="Jobs"
    )


@app.route("/about")
def about():
    quote = get_external_quote()

    return render_template(
        "about.html",
        quote=quote,
        title="About"
    )


@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower()
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(
            "Your account was created successfully. "
            "You can now log in.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form,
        title="Register"
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(
            form.password.data
        ):
            login_user(
                user,
                remember=form.remember.data
            )

            logger.info(
                "Successful login for user: %s",
                user.email
            )

            flash(
                "Welcome back! You have logged in successfully.",
                "success"
            )

            return redirect(url_for("index"))

        logger.warning(
            "Failed login attempt for email: %s",
            email
        )

        flash(
            "Login failed. Please check your email and password.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form,
        title="Login"
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("index"))


@app.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():
    form = UpdateProfileForm(
        original_name=current_user.name,
        original_email=current_user.email
    )

    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(
                form.picture.data
            )

            current_user.image_file = picture_filename

        current_user.name = form.name.data.strip()
        current_user.email = (
            form.email.data.strip().lower()
        )

        db.session.commit()

        flash(
            "Your profile was updated successfully.",
            "success"
        )

        return redirect(url_for("profile"))

    if request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for(
        "static",
        filename=(
            "profile_pics/"
            + current_user.image_file
        )
    )

    return render_template(
        "profile.html",
        form=form,
        image_file=image_file,
        title="Profile"
    )


@app.route(
    "/job/new",
    methods=["GET", "POST"]
)
@login_required
def create_job():
    form = JobForm()

    if form.validate_on_submit():
        job = Job(
            title=form.title.data.strip(),
            company=form.company.data.strip(),
            location=form.location.data.strip(),
            salary=form.salary.data.strip(),
            category=form.category.data,
            short_description=(
                form.short_description.data.strip()
            ),
            full_description=(
                form.full_description.data.strip()
            ),
            author=current_user
        )

        db.session.add(job)
        db.session.commit()

        logger.info(
            "Job added: id=%s, user=%s",
            job.id,
            current_user.email
        )

        flash(
            "The job was published successfully.",
            "success"
        )

        return redirect(
            url_for(
                "job_detail",
                job_id=job.id
            )
        )

    return render_template(
        "create_job.html",
        form=form,
        page_heading="Add a New Job",
        submit_text="Publish Job",
        title="Add Job"
    )


@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = db.get_or_404(Job, job_id)
    delete_form = DeleteJobForm()

    return render_template(
        "job.html",
        job=job,
        delete_form=delete_form,
        title=job.title
    )


@app.route("/user/<string:name>")
def user_jobs(name):
    user = User.query.filter_by(
        name=name
    ).first_or_404()

    jobs = Job.query.filter_by(
        author=user
    ).order_by(
        Job.date_posted.desc()
    ).all()

    image_file = url_for(
        "static",
        filename=(
            "profile_pics/"
            + user.image_file
        )
    )

    return render_template(
        "user_jobs.html",
        user=user,
        jobs=jobs,
        image_file=image_file,
        title=f"{user.name}'s Jobs"
    )


@app.route(
    "/job/<int:job_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_job(job_id):
    job = db.get_or_404(Job, job_id)

    if job.author != current_user:
        abort(403)

    form = JobForm()

    if form.validate_on_submit():
        job.title = form.title.data.strip()
        job.company = form.company.data.strip()
        job.location = form.location.data.strip()
        job.salary = form.salary.data.strip()
        job.category = form.category.data

        job.short_description = (
            form.short_description.data.strip()
        )

        job.full_description = (
            form.full_description.data.strip()
        )

        db.session.commit()

        logger.info(
            "Job edited: id=%s, user=%s",
            job.id,
            current_user.email
        )

        flash(
            "The job was updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "job_detail",
                job_id=job.id
            )
        )

    if request.method == "GET":
        form.title.data = job.title
        form.company.data = job.company
        form.location.data = job.location
        form.salary.data = job.salary
        form.category.data = job.category

        form.short_description.data = (
            job.short_description
        )

        form.full_description.data = (
            job.full_description
        )

    return render_template(
        "create_job.html",
        form=form,
        page_heading="Edit Job",
        submit_text="Save Changes",
        title="Edit Job"
    )


@app.route(
    "/job/<int:job_id>/delete",
    methods=["POST"]
)
@login_required
def delete_job(job_id):
    job = db.get_or_404(Job, job_id)

    if job.author != current_user:
        abort(403)

    form = DeleteJobForm()

    if not form.validate_on_submit():
        abort(400)

    deleted_job_id = job.id

    db.session.delete(job)
    db.session.commit()

    logger.info(
        "Job deleted: id=%s, user=%s",
        deleted_job_id,
        current_user.email
    )

    flash(
        "The job was deleted successfully.",
        "success"
    )

    return redirect(url_for("index"))


@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "404.html",
        error_code=403,
        error_title="Access Denied",
        error_message=(
            "You do not have permission "
            "to perform this action."
        ),
        title="Access Denied"
    ), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        error_code=404,
        error_title="Page Not Found",
        error_message=(
            "The page you are looking for "
            "does not exist."
        ),
        title="Page Not Found"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()

    return render_template(
        "500.html",
        title="Server Error"
    ), 500


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)