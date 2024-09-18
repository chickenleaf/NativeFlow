from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from datetime import datetime

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=user.id, target_lang=user.target_lang)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_translation(db: Session, translation: schemas.TranslationCreate, translated_text: str):
    db_translation = models.Translation(
        id=str(uuid.uuid4()),
        user_id=translation.user_id,
        timestamp=datetime.now(),
        input_text=translation.text,
        translated_text=translated_text
    )
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation

def get_user_translations(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Translation).filter(models.Translation.user_id == user_id).offset(skip).limit(limit).all()