from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    id: str
    target_lang: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    class Config:
        orm_mode = True

class TranslationBase(BaseModel):
    user_id: str
    text: str

class TranslationCreate(TranslationBase):
    pass

class Translation(TranslationBase):
    id: str
    timestamp: datetime
    translated_text: str

    class Config:
        orm_mode = True