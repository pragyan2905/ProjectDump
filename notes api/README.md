# Notes API

A basic modular REST API built with FastAPI, demonstrating JWT authentication and database relationship management. Built for learning purposes.

## Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Database:** SQLite (Zero-config, easily swappable to PostgreSQL)
* **Authentication:** JWT (JSON Web Tokens) with `bcrypt` password hashing
* **Frontend:** Vanilla HTML/JS served via Jinja2 Templates

## Features
* **Modular Architecture:** Complete separation of concerns (Routers, CRUD operations, Schemas, Models, Security).
* **Dependency Injection:** Database sessions and current user state are cleanly injected into endpoints.
* **JWT Auth:** Secure registration and login flow. Passwords are cryptographically hashed using `bcrypt`.
* **Multi-Tenant Data:** Users can only view, create, update, and delete their own notes.

## Project Structure

```text
notes api/
├── app/
│   ├── main.py              # Application entrypoint & UI route
│   ├── database.py          # SQLAlchemy engine & session factory
│   ├── models.py            # Database tables (SQLAlchemy ORM)
│   ├── schemas.py           # Data validation (Pydantic models)
│   ├── crud.py              # Database transactions
│   ├── security.py          # Password hashing & JWT logic
│   ├── routers/
│   │   ├── auth.py          # /api/auth endpoints (Login/Register)
│   │   └── notes.py         # /api/notes endpoints (CRUD)
│   └── templates/
│       └── index.html       # Dynamic frontend UI
├── requirements.txt         # Python dependencies
└── notes.db                 # Auto-generated SQLite database
```

## Setup & Run Instructions

**1. Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the development server:**
```bash
uvicorn app.main:app --reload
```

**4. View the App:**
* **Frontend UI:** Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the full application.
* **Interactive API Docs (Swagger):** Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the REST endpoints directly.

## API Reference

### Authentication (`/api/auth`)
* `POST /register`: Register a new user (requires `email`, `password`).
* `POST /login`: Authenticate and receive a JWT Bearer token.

### Notes (`/api/notes`) - *Requires JWT Header*
* `GET /`: Retrieve all notes belonging to the authenticated user.
* `POST /`: Create a new note.
* `GET /{id}`: Retrieve a specific note.
* `PUT /{id}`: Update a specific note.
* `DELETE /{id}`: Delete a specific note.
