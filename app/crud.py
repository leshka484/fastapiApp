from datetime import date
from fastapi import Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash


# def get_publications(db: Session, skip: int = 0, limit: int = 100):
#     publications = db.query(models.Publication).offset(skip).limit(limit).fi.all()
#     publications_tags = db.query(models.PublicationsTags).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name = user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: Query):
    db.commit()
    db.refresh(db_user)

def delete_user(db: Session, db_user: Query):
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)



def get_publication(db: Session, publication_id: int):
    return db.query(models.Publication).filter(models.Publication.id == publication_id).first()

def create_publication(db: Session, publication: schemas.PublicationCreate, user_id: int):
    db_item = models.Publication(**publication.dict(), owner_id=user_id, publication_date=date.today())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_publication(db: Session, db_publication: Query):
    db.commit()
    db.refresh(db_publication)

def delete_publication(db: Session, db_publication: Query):
    db.delete(db_publication)
    db.commit()
    db.refresh(db_publication)




def create_tag(db: Session, item: schemas.TagsCreate):
    db_item = models.Tags(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
