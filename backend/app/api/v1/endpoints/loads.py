from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.enums import LoadStatus, StopStatus
from app.db.deps import get_db
from app.models.load import Load
from app.models.stop import Stop
from app.schemas.load import LoadCreate, LoadRead
from app.schemas.stop import StopCreate, StopRead

router = APIRouter()


@router.post("/", response_model=LoadRead)
def create_load(payload: LoadCreate, db: Session = Depends(get_db)):
    load = Load(
        organization_id=1,
        created_by_user_id=1,
        external_reference=payload.external_reference,
        customer_name=payload.customer_name,
        status=LoadStatus.planned,
        origin_label=payload.origin_label,
        destination_label=payload.destination_label,
        scheduled_pickup_at=payload.scheduled_pickup_at,
        scheduled_delivery_at=payload.scheduled_delivery_at,
    )
    db.add(load)
    db.commit()
    db.refresh(load)
    return load


@router.get("/", response_model=list[LoadRead])
def list_loads(db: Session = Depends(get_db)):
    return db.query(Load).order_by(Load.created_at.desc()).all()


@router.get("/{load_id}", response_model=LoadRead)
def get_load(load_id: int, db: Session = Depends(get_db)):
    load = db.query(Load).filter(Load.id == load_id).first()
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return load


@router.post("/{load_id}/stops", response_model=StopRead)
def create_stop(load_id: int, payload: StopCreate, db: Session = Depends(get_db)):
    load = db.query(Load).filter(Load.id == load_id).first()
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")

    stop = Stop(
        organization_id=1,
        load_id=load_id,
        facility_id=payload.facility_id,
        stop_number=payload.stop_number,
        stop_type=payload.stop_type,
        status=StopStatus.planned,
        appointment_at=payload.appointment_at,
        current_dwell_minutes=0,
    )
    db.add(stop)
    db.commit()
    db.refresh(stop)
    return stop


@router.get("/{load_id}/timeline")
def get_load_timeline(load_id: int, db: Session = Depends(get_db)):
    load = (
        db.query(Load)
        .options(
            joinedload(Load.stops).joinedload(Stop.facility),
            joinedload(Load.stops).joinedload(Stop.events),
        )
        .filter(Load.id == load_id)
        .first()
    )
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")

    stops = []
    ordered_stops = sorted(load.stops, key=lambda s: s.stop_number)
    for stop in ordered_stops:
        stops.append(
            {
                "stop_id": stop.id,
                "stop_number": stop.stop_number,
                "facility_id": stop.facility_id,
                "facility_name": stop.facility.name if stop.facility else None,
                "status": stop.status,
                "events": [
                    {
                        "event_id": event.id,
                        "event_type": event.event_type,
                        "occurred_at": event.occurred_at,
                        "source": event.source,
                        "idempotency_key": event.idempotency_key,
                    }
                    for event in stop.events
                ],
            }
        )

    return {
        "load_id": load.id,
        "external_reference": load.external_reference,
        "stops": stops,
    }
