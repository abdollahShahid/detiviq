from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.ruleset import Ruleset
from app.schemas.ruleset import RulesetCreate, RulesetRead

router = APIRouter()


@router.post("/", response_model=RulesetRead)
def create_ruleset(payload: RulesetCreate, db: Session = Depends(get_db)):
    ruleset = Ruleset(
        organization_id=1,
        name=payload.name,
        scope_type=payload.scope_type,
        facility_id=payload.facility_id,
        customer_name=payload.customer_name,
        free_minutes=payload.free_minutes,
        grace_minutes=payload.grace_minutes,
        billable_unit_minutes=payload.billable_unit_minutes,
        rate_per_unit=payload.rate_per_unit,
        currency=payload.currency,
        is_active=payload.is_active,
        effective_from=payload.effective_from,
        effective_to=payload.effective_to,
        priority=payload.priority,
    )
    db.add(ruleset)
    db.commit()
    db.refresh(ruleset)
    return ruleset


@router.get("/", response_model=list[RulesetRead])
def list_rulesets(db: Session = Depends(get_db)):
    return db.query(Ruleset).order_by(Ruleset.created_at.desc()).all()
