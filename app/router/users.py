from fastapi import APIRouter, Depends, HTTPException, Path, status
from app import auth, crud, schemas
from app.database import SessionLocal
from app.router.get_db import get_db

router = APIRouter()


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int = Path(), db: SessionLocal = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return user


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def change_user(
    user: schemas.UserCreate, user_id: int = Path(), db: SessionLocal = Depends(get_db)
):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = auth.get_password_hash(user.password)
    crud.update_user(db=db, db_user=db_user)
    return crud.get_user(db=db, user_id=user_id)


@router.delete("/users/{user_id}")
def delete_user(user_id: int = Path(), db: SessionLocal = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    crud.delete_user(db=db, db_user=db_user)
    return {"message": f"user {db_user.name} was deleted"}
