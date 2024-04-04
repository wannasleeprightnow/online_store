from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    is_active: bool = True
    is_superuser: bool = False


class UserRegister(BaseModel):
    username: str
    password: str
    name: str


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    is_active: bool
    is_superuser: bool
