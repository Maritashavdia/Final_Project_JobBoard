# JobBoard

JobBoard is my final project for the Python and Flask course. It is a simple job vacancy website where visitors can view published jobs and read full information about each position.

Users can create an account and log in to the website. After logging in, they can add new job vacancies and update their profile information and profile picture. Each vacancy contains a title, company, location, salary, category, short description, full description, author and publication date.

A user can edit or delete only the vacancies they have published. Other users can view these vacancies, but they cannot change or delete them.

The project was created with Python, Flask, SQLite, SQLAlchemy, Flask-Login, Flask-WTF and Flask-Bcrypt. I used HTML, CSS and Bootstrap for the website design. Requests is used for the external API, Pillow is used for profile pictures and Pytest is used for automated tests.

The About page receives a random motivational quote from an external API. If the API is unavailable, the website displays a default quote instead. The application also records successful and failed logins, added jobs, edited jobs, deleted jobs and API errors in a log file.

The project includes custom 404 and 500 error pages. It also includes three automated tests for the homepage, user login and permission control.

## How to Run the Project

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file and add:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///jobboard.db
```

Run the project:

```bash
python app.py
```

Open the website in the browser:

```text
http://127.0.0.1:5000
```

## Testing

Run the automated tests with:

```bash
pytest -q
```

The website has a friendly and colorful design and works on desktop, tablet and mobile devices.
