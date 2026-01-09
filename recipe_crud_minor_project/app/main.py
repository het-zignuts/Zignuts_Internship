from fastapi import FastAPI
from app.api.recipe_api import router
from app.api.user_api import users_router
from app.auth.routes import auth_router
from app.db.init_db import init_db
# from app.middleware.logging import LoggingMiddleware

app = FastAPI()

# app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()
    
app.include_router(router)
app.include_router(users_router)
app.include_router(auth_router)
