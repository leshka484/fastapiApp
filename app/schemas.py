from datetime import date
from pydantic import BaseModel, EmailStr


class TagsCreate(BaseModel):
    """Проверяет запрос"""

    name: str


class TagsResponse(BaseModel):
    """Формирует ответ"""

    name: str

    class Config:
        orm_mode = True


class PublicationBase(BaseModel):
    title: str
    description: str
    publication_date: date
    tags: list[TagsResponse]


class PublicationResponse(PublicationBase):
    """Формирует ответ"""

    owner_id: int

    class Config:
        orm_mode = True


class PublicationCreate(PublicationBase):
    """Проверяет запрос"""


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Проверяет запрос"""

    password: str


class UserResponse(UserBase):
    """Формирует ответ"""

    id: int
    publications: list[PublicationResponse]
    disabled: bool

    class Config:
        orm_mode = True
