# openssl rand -hex 128
from fastapi import FastAPI
from typing import Optional
import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from tools.connector import ENGINE
from passlib.context import CryptContext
from time import sleep
sleep(3)
# Shared properties


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    pseudo_ig: str = Field(default=None, max_length=255)
    pseudo_di: str = Field(default=None, max_length=255)
    pseudo_li: str = Field(default=None, max_length=255)

# Properties used by api


class UserInput(UserBase):
    password: str = Field(min_length=8, max_length=40)

# Database model, database table inferred from class name


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = False
    is_superuser: bool = False


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


app = FastAPI()

SQLModel.metadata.create_all(ENGINE)


@app.get("/users/", response_model=list[User])
def get_users():
    return [User(email="test@test.com", hashed_password="test")]


@app.post("/users/", response_model=User)
def create_user(new_user: UserInput):
    # created =
    return User(
        email=new_user.email,
        pseudo_di=new_user.pseudo_di,
        pseudo_ig=new_user.pseudo_ig,
        pseudo_li=new_user.pseudo_li,
        is_active=True
    )
