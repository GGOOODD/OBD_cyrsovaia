from pydantic import BaseModel


class RegInfo(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
    password: str
    repeat_password: str


class LogInfo(BaseModel):
    email: str
    password: str


class GetUser(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
