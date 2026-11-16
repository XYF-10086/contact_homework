# Contact Homework — Contact Management System

## 1. Project Introduction

This project is a contact management web application developed for the Extreme Programming (XP) assignment.

The application provides contact management, multiple contact methods, favorite contacts, and Excel import/export functionality.

## 2. Project Structure

```text
contact_homework/
├── index.html
├── script.js
├── style.css
└── task_b_contact_backend/
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── schemas.py
    │   ├── contact_service.py
    │   └── excel_service.py
    ├── tests/
    ├── docs/
    ├── requirements.txt
    └── README.md
```

## 3. Main Features

- Contact creation, editing, deletion and searching.
- Multiple phone numbers, email addresses, social accounts and addresses.
- Favorite contact management.
- Excel contact import and export.
- Persistent data storage using SQLite.

## 4. Technologies

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- FastAPI
- SQLite
- OpenPyXL
- Pydantic

## 5. Backend Setup

Enter the backend directory:

```bash
cd task_b_contact_backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

## 6. Team Responsibilities

- Task A: Frontend development, user interface and favorites interface.
- Task B: Backend development, contact data management, multiple contact methods and Excel import/export.

## 7. Testing

Run backend tests:

```bash
pytest -q
```

For detailed backend documentation, see `task_b_contact_backend/README.md`.
