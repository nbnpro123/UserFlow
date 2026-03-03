from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional

class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    age:int = Field(..., gt=0, le=150, description='Возраст от 1 до 150')
    email: EmailStr


    @validator('name')
    def name_validator(cls, v):
        if not v[0].isalpha():
            raise ValueError('Имя должно начинаться с заглавной буквы')
        return v

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, gt=0, le=150)
    email: Optional[EmailStr] = None