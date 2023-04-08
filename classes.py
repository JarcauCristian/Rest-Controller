from pydantic import BaseModel

class Signup(BaseModel):
    username: str
    password: str
    email: str


class Signin(BaseModel):
    username: str
    password: str


class Transaction(BaseModel):
    database_name: str


class PasswordReset(BaseModel):
    current_password: str
    new_password: str


class Validate(BaseModel):
    code: str
    email: str


class Balance(BaseModel):
    balance: float


class Delete(BaseModel):
    email: str