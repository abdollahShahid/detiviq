from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.detention_case import DetentionCase
from app.schemas.detention_case import DetentionCaseRead

router = APIRouter()


@router.get("/", response_model=list[DetentionCaseRead])
def list_detention_cases(db: Session = Depends(get_db)):
    return (
        db.query(DetentionCase)
        .order_by(DetentionCase.created_at.desc(), DetentionCase.id.desc())
        .all()
    )
