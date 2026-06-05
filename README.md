# Library Management System

A Django-based Library Management System with a split frontend/backend structure.

## Project Structure

```
library_split_frontend_backend/
├── backend/          ← Django project (manage.py lives here)
│   ├── library/      ← Main app (models, views, forms)
│   ├── librarymanagement/  ← Django settings, urls, wsgi
│   ├── requirements.txt
│   └── .env.example
└── frontend/         ← HTML templates + static assets
    ├── templates/
    └── static/
```

## Setup & Run

### Prerequisites
- Python 3.10+

### Steps

**1. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**3. Apply database migrations**

```bash
python manage.py migrate
```

**4. Create an admin (superuser) account**

```bash
python manage.py createsuperuser
```

**5. Run the development server**

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Accounts

| Role    | How to create                                   | Login URL          |
|---------|-------------------------------------------------|--------------------|
| Admin   | `python manage.py createsuperuser`              | /adminclick → Login |
| Student | Register via the Student → Sign Up page         | /studentclick      |

---

## Email (optional)

The Contact Us page sends email via Gmail SMTP.  
To enable it, copy `backend/.env.example` to `backend/.env` and fill in your Gmail credentials (use an App Password, not your regular password).

Without email configured, the Contact Us form will raise an error — all other features work fine without it.

---

## Notes

- The database is SQLite (`backend/db.sqlite3`), created automatically on first migration.
- `DEBUG=True` and `ALLOWED_HOSTS=['*']` are set for local development only.
