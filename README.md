
# Inventory Management API

This project is a RESTful API built using **FastAPI** to manage an inventory system. It supports CRUD operations, and integration with a PostgreSQL database. The API is also equipped with automated tests using `pytest`.

## Features

- **CRUD Operations**:
  - Create, Read, Update, and Delete inventory items.
- **Database Integration**:
  - PostgreSQL for data persistence.
- **Automated Testing**:
  - Unit tests for API endpoints using `pytest`.

## Prerequisites

- **Python 3.11 or higher**.
- **PostgreSQL** installed and running.
- **pip** for dependency management.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/inventory-api.git
   cd inventory-api
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Linux/Mac
   .\venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**:
   - Create a PostgreSQL database:
     ```sql
     CREATE DATABASE inventory_db;
     ```
   - Update the `DATABASE_URL` in `main.py`:
     ```python
     DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/inventory_db"
     ```

## Running the Application

1. **Run the API**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:
   - Root URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Swagger UI (Interactive Documentation): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc Documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running Tests

1. **Run All Tests**:
   ```bash
   pytest
   ```

2. **Test Coverage**:
   Add the `pytest-cov` plugin for test coverage:
   ```bash
   pip install pytest-cov
   pytest --cov=.
   ```

## Project Structure

```
inventory-api/
├── main.py                  # FastAPI application
├── models.py                # SQLAlchemy models
├── tests/
│   └── test_main.py         # Unit tests
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```
