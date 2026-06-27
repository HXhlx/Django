# Personal Information Management System

A Django-based personal information management system with user registration/login, profile management, and schedule management.

## Features

- User registration and login
- View and edit personal information
- Schedule CRUD (Create, Read, Update, Delete)
- Schedule search and pagination
- Bilingual support (Chinese/English)

## Quick Start

```bash
# Install dependencies
uv sync

# Initialize database
uv run python manage.py migrate

# Create admin user
uv run python manage.py createsuperuser

# Start server
uv run python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Configuration

Copy `.env.example` to `.env` and modify as needed.

## Tech Stack

- Python 3.12+
- Django 6.0
- Bootstrap 5
- SQLite (default) / MySQL / PostgreSQL

## Internationalization

The system supports Chinese and English. Use the language switcher in the navigation bar to toggle between languages.

## License

MIT
