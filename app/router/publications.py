from fastapi import APIRouter, Depends, HTTPException, Path, status
from app import crud, schemas
from app.router.get_db import get_db
from app.database import SessionLocal

router = APIRouter()

@router.get("/publications/{publication_id}", response_model=schemas.PublicationResponse)
def get_publication(publication_id: int = Path(), db: SessionLocal = Depends(get_db)):
    publication = crud.get_publication(db=db, publication_id=publication_id)
    if not publication:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication does not exist")
    return publication

@router.post("/publications/",response_model=schemas.PublicationResponse)
def create_publication(publication: schemas.PublicationCreate, db: SessionLocal = Depends(get_db)):
    # if not crud.get_publication(db=db, publication_id=publication.id):
    #     return HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Publication does not exist")
    return crud.create_publication(publication=publication, db=db, user_id=1) #Добавить получение id юзера
    # при добавлении записи должны создаваться теги?

@router.put("/publications/{publication_id}", response_model=schemas.PublicationResponse)
def change_publication(publication: schemas.PublicationCreate, user_id: int, publication_id: int = Path(), db: SessionLocal = Depends(get_db)):
    db_publication = crud.get_publication(db=db, publication_id=publication_id)
    if not publication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication does not exist")
    if db_publication.owner_id == user_id:
        db_publication.title = publication.title
        db_publication.description = publication.description
        db_publication.tags = publication.tags
        crud.update_publication(db=db, db_publication=db_publication)
        return crud.get_publication(db=db, publication_id=publication_id)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot modify this publication")

@router.delete("/publications/{publication_id}")
def delete_publication(user_id: int, publication_id: int = Path(), db: SessionLocal = Depends(get_db)):
    db_publication = crud.get_publication(db=db, publication_id=publication_id)
    if not db_publication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication does not exist")
    if db_publication.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot modify this publication")
    crud.delete_publication(db=db, db_publication=db_publication)
    return {"message": f"publication {db_publication.title} was deleted"}