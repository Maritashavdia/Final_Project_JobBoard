# JobBoard

JobBoard is my final project for the Python and Flask course. It is a responsive web application where visitors can browse job vacancies, filter them by category and open a separate page with full information about each position.

Live website: [final-project-jobboard.onrender.com](https://final-project-jobboard.onrender.com/)

## Main Features

- User registration, login and logout
- Secure password hashing with Flask-Bcrypt
- User profile and profile-picture update
- Creation, viewing, editing and deletion of job vacancies
- Permission control: users can edit or delete only their own vacancies
- Job filtering by category
- Automatic sorting by publication date, with the newest jobs shown first
- Separate pages for the jobs published by each user
- Random motivational quote from an external API
- Default quote when the external API is unavailable
- Custom 403, 404 and 500 error handling
- File logging for the required application events
- Automated tests for the main routes and permission control
- Responsive interface built with Jinja2, Bootstrap and custom CSS

## Technologies Used

- Python and Flask
- SQLAlchemy and Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Bcrypt
- SQLite for local development
- PostgreSQL for production on Render
- Requests for external API integration
- Pillow for profile-image processing
- Pytest for automated testing
- HTML, Jinja2, CSS and Bootstrap
- Gunicorn for production deployment

## Database Models

The application contains two main models:

- `User` stores the user's name, email, hashed password and profile image.
- `Job` stores the title, company, location, salary, category, descriptions, publication date and author.

The models have a one-to-many relationship: one user can publish multiple jobs, while each job belongs to one user.

## Permissions

Creating a vacancy requires authentication. Before editing or deleting a vacancy, the application checks whether the current user is its author. Unauthorized users receive a `403 Forbidden` response and cannot modify another user's data.

## External API

The About page requests a random motivational quote from DummyJSON. The request has a timeout and error handling. If the request fails, the application displays a local default quote, so the page continues to work.

## Logging

Python's `logging` module writes the following required events to `jobboard.log`:

- Successful login
- Failed login attempt
- Job creation
- Job editing or deletion
- External API request error

Passwords and other sensitive information are not written to the log file.

## Project Structure

```text
Final_Project_JobBoard/
├── static/             # CSS, images and profile pictures
├── templates/          # Jinja2 HTML templates
├── tests/              # Automated tests
├── app.py              # Routes and application logic
├── config.py           # Application configuration
├── forms.py            # WTForms classes and validation
├── models.py           # Database models
├── requirements.txt    # Python dependencies
└── README.md
```

## How to Run the Project Locally

1. Create a virtual environment:

```powershell
py -m venv .venv
```

2. Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project directory:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///jobboard.db
```

5. Start the application:

```powershell
python app.py
```

6. Open `http://127.0.0.1:5000` in a browser.

## Automated Tests

Run the tests from the project directory:

```powershell
pytest -q
```

The test suite checks:

- The home page route
- Successful user login
- Permission protection preventing another user from editing or deleting a vacancy

## Deployment

The application is deployed on Render. The production version uses Gunicorn as the WSGI server and PostgreSQL as the database. Environment variables are configured on Render and are not stored directly in the repository.
