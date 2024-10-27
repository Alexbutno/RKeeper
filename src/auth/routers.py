from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.schemas import EmailValidation
from src.utils import create_jwt_token, validate_tmp_token, create_tmp_token, generate_secret_code
from src.utils import get_db_manager, hash_password, verify_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    db_manager = await get_db_manager()
    user = await db_manager.get_user_by_email(form_data.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = await hash_password(form_data.password)

    secret_code = generate_secret_code()
    token_expires_at = int(datetime.now().timestamp()) + 300
    user_id = await db_manager.create_tmp_user(email=form_data.username, hashed_password=hashed_password,
                                               validation_start_timestamp=token_expires_at, token=secret_code)
    token = await create_tmp_token(str(user_id), secret_code, token_expires_at)
    return {"message": "User created, waiting for verification", "token": token}


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_manager = await get_db_manager()
    user_data = await db_manager.get_user_by_email(form_data.username)

    hashed_password = await hash_password(form_data.password)
    if user_data is None or not await verify_password(form_data.password, hashed_password):  #
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = await create_jwt_token(str(user_data.id))
    return {"access_token": token, "token_type": 'bearer'}


@router.post("/email_validation")
async def email_validation(data: EmailValidation):
    payload = await validate_tmp_token(data.token)
    print(payload)
    generated_code = payload['secret_code']
    user_code = data.secret_code
    token_expiratioin_timestamp = payload['token_exp_timestamp']
    if int(datetime.now().timestamp()) > token_expiratioin_timestamp:
        raise HTTPException(status_code=400, detail="Confirmation code expired")

    if user_code != generated_code:
        raise HTTPException(status_code=400, detail="Incorrect confirmation code")

    db_manager = await get_db_manager()
    username, hashed_pass = await db_manager.get_tmp_user_data(payload['user_id'])
    user_id = await db_manager.create_user(email=username, hashed_password=hashed_pass)
    token = await create_jwt_token(str(user_id))
    await db_manager.delete_nonvalid_user_by_uuid(payload['user_id'])
    return {"message": "User created successfully", "token": token}

    # токены на этот запрос должны содержать в payloade пометку что это временный токен
    # сюда мне нужна отдельная валидация токена, а в decode_jwt_token поднимать ошибку, если это тестовый
    # тут валидирую токен, если он правильный -- добавляю в основную таблицу этого пользователя
    # удаляю из tmp таблицы пользователя по заданному uuid
