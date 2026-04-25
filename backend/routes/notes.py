from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database import get_db
from backend import models, schemas
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])


def get_or_create_tag(db: Session, tag_name: str) -> models.Tag:
    
    tag = db.query(models.Tag).filter(models.Tag.name == tag_name.lower()).first()
    if not tag:
        tag = models.Tag(name=tag_name.lower())
        db.add(tag)
        db.flush()
    return tag


@router.post("/", response_model=schemas.NoteOut, status_code=201)
def create_note(
    note_data: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_note = models.Note(
        title=note_data.title,
        content=note_data.content,
        folder=note_data.folder or "Genel",
        user_id=current_user.id
    )

    
    for tag_name in note_data.tags:
        tag = get_or_create_tag(db, tag_name)
        new_note.tags.append(tag)

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(
    search: Optional[str] = Query(None, description="Başlık veya içerikte arama"),
    folder: Optional[str] = Query(None, description="Klasöre göre filtrele"),
    tag: Optional[str] = Query(None, description="Etikete göre filtrele"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Note).filter(models.Note.user_id == current_user.id)

    if search:
        query = query.filter(
            models.Note.title.ilike(f"%{search}%") |
            models.Note.content.ilike(f"%{search}%")
        )

    if folder:
        query = query.filter(models.Note.folder == folder)

    if tag:
        query = query.filter(
            models.Note.tags.any(models.Tag.name == tag.lower())
        )

    return query.order_by(models.Note.created_at.desc()).all()


@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return note


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note_data: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")

    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    if note_data.folder is not None:
        note.folder = note_data.folder

    if note_data.tags is not None:
        note.tags = []
        for tag_name in note_data.tags:
            tag = get_or_create_tag(db, tag_name)
            note.tags.append(tag)

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")

    db.delete(note)
    db.commit()


@router.get("/folders/list")
def get_folders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Kullanıcının tüm klasörlerini listele."""
    folders = db.query(models.Note.folder).filter(
        models.Note.user_id == current_user.id
    ).distinct().all()
    return {"folders": [f[0] for f in folders if f[0]]}