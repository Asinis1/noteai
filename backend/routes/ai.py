from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import models, schemas
from backend.routes.auth import get_current_user
from backend.ai_service import analyze_note
from backend.routes.notes import get_or_create_tag

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/analyze/{note_id}", response_model=schemas.AIAnalysisResult)
def analyze(
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

    
    try:
        result = analyze_note(note.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analizi başarısız: {str(e)}")

    
    note.summary = result.get("summary", "")
    note.keywords = ", ".join(result.get("keywords", []))

    
    existing_tag_names = {tag.name for tag in note.tags}
    for tag_name in result.get("suggested_tags", []):
        if tag_name.lower() not in existing_tag_names:
            tag = get_or_create_tag(db, tag_name)
            note.tags.append(tag)

    db.commit()
    db.refresh(note)

    return schemas.AIAnalysisResult(
        summary=result.get("summary", ""),
        suggested_tags=result.get("suggested_tags", []),
        keywords=result.get("keywords", [])
    )