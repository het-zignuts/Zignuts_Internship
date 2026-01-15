# Recipe Management API (CRUD)

## Tech Stack

* **Python** (3.14.x)
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **SQLModel**
* **SQLite**
* **JWT Authentication**
* **Role-Based Access Control (RBAC)**
* **Pytest** (Unit Testing)

---

## Key Features

* RESTful API design using **FastAPI**
* Full **CRUD operations** for recipes
* **JWT-based authentication** (Access & Refresh tokens)
* **Role-based authorization** (User / Admin)
* Secure route protection using dependencies
* Persistent storage using **SQLite**
* Data validation with **Pydantic & SQLModel**
* Clean separation of concerns (API / CRUD / DB / Schemas)
* Automatic timestamps (`created_at`, `updated_at`)
* Unit & integration tests using **pytest**

---

## Project Structure

```text
recipe_crud
├── app/
│   ├── api/
│   │   ├── auth.py            # Authentication routes
│   │   ├── recipes.py         # Recipe CRUD routes
│   │   └── __init__.py
│   ├── auth/
│   │   ├── deps.py            # Auth dependencies
│   │   └── jwt.py             # JWT utilities
│   ├── crud/
│   │   ├── recipe.py          # Recipe business logic
│   │   └── user.py
│   ├── models/
│   │   ├── recipe.py          # SQLModel Recipe ORM
│   │   └── user.py
│   ├── schemas/
│   │   ├── recipe.py          # Pydantic schemas
│   │   └── user.py
│   ├── core/
│   │   ├── config.py          # App configuration
│   │   ├── security.py        # Password hashing & JWT
│   │   └── enums.py           # Enums (Category, Role)
│   ├── db/
│   │   ├── session.py         # DB session manager
│   │   └── init_db.py         # DB initialization
│   ├── main.py                # FastAPI entry point
│   └── __init__.py
├── tests/
│   ├── test_auth.py
│   ├── test_recipe.py
│   ├── test_user.py
│   └── conftest.py
├── requirements.txt
└── README.md
```

---

## Recipe Model (Core Fields)

Each recipe contains the following essential fields:

* `id` – UUID (Primary Key)
* `title` – Recipe name
* `description` – Short description
* `ingredients` – List of ingredients (stored as JSON in SQLite)
* `instructions` – Cooking steps (plain string)
* `time_taken` – Preparation time (minutes, integer)
* `category` – Enum (e.g., VEG / NON_VEG / VEGAN)
* `cuisine` – String (e.g., Indian, Italian)
* `owner_id` – User who created the recipe
* `created_at` – Auto-set on creation
* `updated_at` – Auto-updated on modification

---

## Authentication & Authorization

### JWT Authentication

* Secure login using email & password
* Generates **Access Token** and **Refresh Token**
* Tokens include:

  * `sub` → User ID
  * `role` → User role
  * `exp` → Expiration time

### Role-Based Access Control

* **User**:

  * Create recipes
  * Read own recipes
  * Update/Delete own recipes
* **Admin**:

  * Full access to all recipes
  * Manage users

Route protection is handled via FastAPI dependencies.

---

## API Endpoints

### Authentication

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| POST   | `/auth/register` | Register new user    |
| POST   | `/auth/login`    | Login & get tokens   |
| POST   | `/auth/refresh`  | Refresh access token |

### Recipes

| Method | Endpoint        | Description      |
| ------ | --------------- | ---------------- |
| POST   | `/recipes/`     | Create recipe    |
| GET    | `/recipes/`     | List recipes     |
| GET    | `/recipes/{id}` | Get recipe by ID |
| PUT    | `/recipes/{id}` | Replace recipe   |
| PATCH  | `/recipes/{id}` | Partial update   |
| DELETE | `/recipes/{id}` | Delete recipe    |

---

## Database

* Uses **SQLite** for simplicity
* SQLModel ORM ensures:

  * SQL injection protection
  * Strong typing
  * Automatic schema generation
* Ingredients stored as JSON-compatible list
* Data persists across server restarts

---

## Testing

* Tests written using **pytest**
* Includes:

  * Authentication tests
  * Authorization checks
  * Recipe CRUD tests
* Uses a separate **test database**
* Dependency overrides for DB session isolation

Run tests:

```bash
pytest -v
```

---

## Setup & Installation

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Environment

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Design Philosophy

* Keep things **simple & SQLite-friendly**
* Avoid overengineering
* Clear separation of layers
* Explicit security checks
* Easy to extend to Postgres later

---

### Author

**Het Shukla**

---

> This project focuses on correctness, clarity, and real-world backend practices rather than unnecessary complexity.
