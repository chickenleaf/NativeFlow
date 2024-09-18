from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, translator
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.post("/translate/", response_model=schemas.Translation)
def translate_text(translation: schemas.TranslationCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=translation.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    translator_instance = translator.ConversationTranslator()
    translated_text = translator_instance.translate(translation.text, translation.user_id)
    
    return crud.create_translation(db=db, translation=translation, translated_text=translated_text)

@app.get("/users/{user_id}/translations/", response_model=list[schemas.Translation])
def read_user_translations(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    translations = crud.get_user_translations(db, user_id=user_id, skip=skip, limit=limit)
    return translations