# BOOKS COLLECTION - CRUD (in - memory) 

## Tech-Stack:
- Python (3.14.2)
- FastAPI
- Uvicorn
- Pydantic

## Key Features:
- Robust API design using FastAPI
- Routing and Exception Handling
- Persistent data storage (SQLite)
- CRUD + Validation using SQLModel
- Seperate handling of business logic
- Isolation of Path operations from business logic
- API creation for CRUD on books
- Retrieving books based on author passed as query parameter
- Dependency Injection for DB session management
- Centralized request–response logging via middleware

## Project Structure:
```text
book_collection_crud_np
├── app/
│   ├── api/
│   │   ├── books_api.py (API routes)
│   │   └── __init__.py
│   ├── crud/
│   │   ├── books_crud.py (Business Logic)
│   │   └── __init__.py
│   ├── schema/
│   │   ├── books_schema.py (Pydantic Schema)
│   │   └── __init__.py
│   ├── db/
│   │   ├── books_db.py (ORM Model based on SQLModel)
│   │   ├── session.py (Session Management)
│   │   ├── init_db.py (Database Initializaton)
│   │   └── __init__.py
│   ├── middleware/
│   │   └── logging/
│   │       └── req_resp_logs.py  (Custom request/response logging middleware)
│   ├── main.py (Entry Point)
│   └── __init__.py
├── requirements.txt 
└── README.md
```

## Project and Environment Setup:

- Project Requirements:
```text
- Python (3.14.x)
- uvicorn 
- FastAPI
- SQLModel
```

- Environment Setup:

1. Create a new env in project folder `books_collect_crud_np`:
```bash
python -m venv .venv
```

2. Activate the environemnt:
```bash
source .venv/bin/activate
```

3. Intsall the dependencies:
```bash
pip install -r requirements.txt
```

4. Running the server:
```bash
uvicorn app.main:app --reload
```
The server starts running on (https://127.0.0.1:8000)

## API Endpoints (specified in app.api.books_api.py)

| **Request Pattern** | **Method** | **Operation** | **Remarks**| **Path Operation**|
|--------------|------------|---------------|------------|-------------|
| /books/{books_id}| GET | Retrieve a book by ID | - | api_get_book(...)|
| /books/{books_id} | PUT | Update/Replace a book (PUT) | - | api_update_book(...)|
| /books/{books_id} | PATCH | Partial update of a book | - | api_partial_update_books(...)|
| /books/{books_id} | DELETE | DELETE a book wih specified ID | - | api_delete_book(...)|
| /books/ | POST | Create a new book | - | api_create_book(...)|
| /books?author=... | GET | List books by the author specified in query| Returns all books for `author=None` | api_list_books(...)|

#### You can check the API endpoints and test them at (https://127.0.0.1:8000/docs) while running the app.

## Data Storage (Persistent Database):
Data is stored in a relational database using SQLModel.
Default database: SQLite
ORM models are defined in app.db.books_db.py. Database engine & session management live in app.db.session.py.
Data persists across server restarts

## Validation using Pydantic/SQLModel:
The module app.schema.books_schema.py defines the pydantic schema for the incoming requests for Updata, Partial Updata, and Creat Operations by inheriting the BaseModel for Validating the fields.It internally uses python type hinting for validation

#### Response validation is also done by BookResponse Schema which serializes the data fro raw model objects to form proper validated output that should be shared to the client, preventing, also, the comprise in security by data exposure happening otherwise.

## Business Logic for CRUD:
This resides in the module app.crud.books_crud.py which finally interacts with the data storage and performs necessary data retrieval, modification, creation, deletion, etc. 
The seperation of this business logic from the API logic ensures modularity, ease in unit-testing, change in DB platforms, scaling, etc.

## Database Safety & Integrity:
- SQL injection protection via ORM parameter binding
- Atomic transactions to avoid partial writes
- Controlled session lifecycle per request
- Explicit refresh of ORM objects after commits

## Routing: 
It is handled by APIRouter of FastAPI whose instance is registered in main.py... URLDispatching is handled by this.

## Middleware:
A custom middleware is used to log request/response cycle. It monitors and tracks each request/response and logs the following:
- HTTP method
- Request URL
- Query parameters
- Headers
- Client IP
- Response status code
- Response headers
- Processing time per request

## The main.py serves as the entry point with the FastAPI instance `app`.

## Check out the docs for FastAPI [here](https://fastapi.tiangolo.com/).
### Author:  
#### Het Shukla
