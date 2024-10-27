from pydantic import BaseModel


class Auth(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class EmailValidation(BaseModel):
    token: str
    secret_code: int
