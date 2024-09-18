from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    target_lang = Column(String)

    translations = relationship("Translation", back_populates="user")

class Translation(Base):
    __tablename__ = "translations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime)
    input_text = Column(String)
    translated_text = Column(String)

    user = relationship("User", back_populates="translations")