from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, security
from ..database import get_db

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"]
)

@router.post("/", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_note(db=db, note=note, user_id=current_user.id)

@router.get("/", response_model=List[schemas.NoteResponse])
def read_notes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    notes = crud.get_notes(db, user_id=current_user.id, skip=skip, limit=limit)
    return notes

@router.get("/{note_id}", response_model=schemas.NoteResponse)
def read_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_note = crud.get_note(db, note_id=note_id, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int, 
    note: schemas.NoteCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_note = crud.update_note(db, note_id=note_id, note_data=note, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/{note_id}")
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_note = crud.delete_note(db, note_id=note_id, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
