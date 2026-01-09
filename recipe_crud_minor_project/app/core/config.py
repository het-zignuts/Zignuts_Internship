import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'wehfew78&79G&*897*8i^&*BBJ')
    REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY', 'euuih9*%^&^*HJhhmnkjkjjj')
    TOKEN_EXPIRY_TIME = os.getenv('TOKEN_EXPIRY_TIME', 30) # minutes
    REFRESH_TOKEN_EXPIRY_TIME = os.getenv('REFRESH_TOKEN_EXPIRY_TIME', 10) # days
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
