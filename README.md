# Track Your Products – Backend

Backend application for **Track Your Products**, a web application designed to track product prices across online stores.

This repository contains the backend responsible for user management, authentication, password recovery and the core API infrastructure.

## Features

### Authentication
- User registration.
- Email verification using temporary verification codes.
- User login.
- JWT authentication.
- Token validation.
- Password recovery through email verification.
- Password reset using temporary tokens.

### API
- REST API built with Django Ninja Extra.
- Request and response validation using schemas.
- Organized backend architecture separating controllers, services, utilities and schemas.

## Technologies

- **Python** – Main programming language.
- **Django** – Backend framework.
- **Django Ninja Extra** – API development and controller management.
- **Django Ninja JWT** – JWT authentication.
- **PostgreSQL** – Database.
- **pgvector** – Vector data support.
- **Pydantic** – Data validation.
- **Playwright** – Browser automation and web data extraction.

## Project Structure

```text
backend/
│
├── users/
│   ├── controllers/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   ├── models.py
│   └── ...
│
├── products/
│   ├── controllers/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   ├── models.py
│   └── ...
│
├── config/
│
├── manage.py
├── requirements.txt
└── .env
```

## Requirements

- Python 3.15 or newer.
- PostgreSQL.
- pip.
- Git.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/naykobye-netizen/Track-Your-Products.git
cd Track-Your-Products/backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the backend root directory.

Configure the required environment variables, including:

- Django secret key.
- Debug mode.
- Allowed hosts.
- PostgreSQL database credentials.
- Email configuration.
- JWT settings, if customized.

Do not commit your `.env` file to the repository.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The backend will be available at:

`http://127.0.0.1:8000/`

## API Documentation

The API documentation is available through the Swagger interface provided by Django Ninja Extra.

Once the development server is running, access the API documentation through the configured documentation endpoint.

## Versioning

The project follows Semantic Versioning.

Current version: **0.2.0**

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

License not specified yet.