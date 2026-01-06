from fastapi import FastAPI
from app.api.books_api import router

app = FastAPI()

app.include_router(router)