from typing import Annotated
from fastapi import FastAPI, Depends
from src.database import SessionLocal
from src import schemas, models
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: db_dependency):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users', response_model=list[schemas.User])
def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users


@app.post('/posts/{user_id}', response_model=schemas.Post)
def create_post(user_id: int, post: schemas.PostCreate, db: db_dependency):
    new_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 
