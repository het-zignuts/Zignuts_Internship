from fastapi import FastAPI
from app.api.books_api import router
from app.db.init_db import init_db
from app.middleware.logging.req_resp_logs import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()
    
app.include_router(router)