import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '12w2dhhd12@@!&**@jhhjhj')
    REFRESH_SECRET_KEY=os.getenv('REFRESH_SECRET_KEY', '17361238bg&*&*U^VFuu')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    TOKEN_EXPIRY_TIME = int(os.getenv('TOKEN_EXPIRY_TIME', 15)) # minutes
    REFRESH_TOKEN_EXPIRY_TIME = int(os.getenv('REFRESH_TOKEN_EXPIRY_TIME', 30)) # days
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')