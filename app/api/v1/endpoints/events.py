from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventRead

router = APIRouter()


@router.post("/", response_model=EventRead)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    if payload.idempotency_key:
        existing = (
            db.query(Event)
            .filter(
                Event.organization_id == 1,
                Event.idempotency_key == payload.idempotency_key,
            )
            .first()
        )
        if existing:
            return existing

    event = Event(
        organization_id=1,
        load_id=payload.load_id,
        stop_id=payload.stop_id,
        event_type=payload.event_type,
        occurred_at=payload.occurred_at,
        source=payload.source,
        idempotency_key=payload.idempotency_key,
        payload_json=payload.payload_json,
        ingested_by_user_id=1,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.occurred_at.asc(), Event.id.asc()).all()
