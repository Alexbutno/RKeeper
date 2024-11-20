import os
from dotenv import load_dotenv

load_dotenv()

SECRET_JWT_KEY = os.getenv('SECRET_JWT_KEY')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_PASS = os.getenv('DB_PASS')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
SENDER_MAIL = os.getenv('SENDER_MAIL')
PASSWORD_MAIL = os.getenv('PASSWORD_MAIL')


ALEMBIC_URL = f''
