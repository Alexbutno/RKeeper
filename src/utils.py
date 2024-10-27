import hashlib
import logging

import jwt
from fastapi import HTTPException
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT
from src.config import MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB_NAME
from src.config import SECRET_JWT_KEY
from src.db_manager_mongo import DBManagerMongo
from src.db_manager_postgres import DBManagerPostgres

DATABASE_URL = f"postgresql+asyncpg://{DB_NAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_USER}?async_fallback=True"

engine = create_async_engine(DATABASE_URL,
                             connect_args={
                                 "ssl": False
                             })
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # NOQA


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_db_manager() -> DBManagerPostgres:
    async with async_session_maker() as session:
        return DBManagerPostgres(session)


logging.basicConfig(level=logging.INFO)

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/mongodb"
connection = MongoClient(MONGO_URL, authSource="admin")


async def get_mongo_db_manager() -> DBManagerMongo:
    return DBManagerMongo(connection.get_database(MONGO_DB_NAME))


async def create_jwt_token(user_id: str) -> str:
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_JWT_KEY, algorithm="HS256")
    return token


async def decode_jwt_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=["HS256"])
    if payload.get("type", None) is not None:
        raise HTTPException(status_code=400, detail="Invalid jwt token")
    return payload


async def create_tmp_token(user_id: str, secret_code: int, token_exp_timestamp: int) -> str:
    payload = {
        "type": "tmp",
        "user_id": user_id,
        "secret_code": secret_code,
        "token_exp_timestamp": token_exp_timestamp
    }
    token = jwt.encode(payload, SECRET_JWT_KEY, algorithm="HS256")
    return token


async def validate_tmp_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=["HS256"])
    if payload.get("type", None) != "tmp":
        raise HTTPException(status_code=400, detail="Invalid jwt token")
    return payload


async def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password


async def verify_password(password: str, hashed_password: str) -> bool:
    return await hash_password(password) == hashed_password


def generate_secret_code():
    from random import randint
    a = randint(0, 10000)
    print(a)
    return a
