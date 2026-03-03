# schemas.py
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional

class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    age: int = Field(..., gt=0, le=150, description="Возраст от 1 до 150")
    email: EmailStr

    # Пример валидатора для дополнительной логики
    @validator('name')
    def name_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError('Имя должно начинаться с заглавной буквы')
        return v

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, gt=0, le=150)
    email: Optional[EmailStr] = None

    # Можно добавить валидатор, который проверяет, что хотя бы одно поле передано
    @validator('name', 'age', 'email', always=True)
    def check_at_least_one(cls, v, values, **kwargs):
        if not any([values.get('name'), values.get('age'), values.get('email')]):
            raise ValueError('Должно быть указано хотя бы одно поле для обновления')
        return v