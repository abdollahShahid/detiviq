from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.facility import Facility
from app.schemas.facility import FacilityCreate, FacilityRead

router = APIRouter()


@router.post("/", response_model=FacilityRead)
def create_facility(payload: FacilityCreate, db: Session = Depends(get_db)):
    facility = Facility(
        organization_id=1,
        name=payload.name,
        code=payload.code,
        customer_name=payload.customer_name,
        timezone=payload.timezone,
        city=payload.city,
        state=payload.state,
        is_active=True,
    )
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


@router.get("/", response_model=list[FacilityRead])
def list_facilities(db: Session = Depends(get_db)):
    return db.query(Facility).order_by(Facility.created_at.desc()).all()
