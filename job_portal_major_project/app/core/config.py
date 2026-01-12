import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY', 'hjhiued*^@**(#HGHJKghjj)')
    REFRESH_SECRET_KEY=os.getenv('REFRESH_SECRET_KEY', 'fgufyud^*&I^%@jhhhk&*^&8778jhh')
    DATABASE_URL=os.getenv('DATABASE_URL','postgresql+psycopg2://job_user:job_board%23project@localhost:5432/job_board')
    # TEST_DATABASE_URL=os.getenv('TEST_DATABASE_URL','postgresql+psycopg2://job_user:job_board%23project@localhost:5432/test_job_board')
    TEST_DATABASE_URL='postgresql+psycopg2://job_test_user:test_password@localhost:5432/job_board_test'
    TOKEN_EXPIRY_TIME=os.getenv('TOKEN_EXPIRY_TIME', '30')  # in minutes
    REFRESH_TOKEN_EXPIRY_TIME=os.getenv('REFRESH_TOKEN_EXPIRY_TIME', '20')  # in days
    ALGORITHM=os.getenv('ALGORITHM', 'HS256')