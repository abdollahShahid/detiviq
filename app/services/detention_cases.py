from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.detention_case import DetentionCase
from app.models.load import Load
from app.models.stop import Stop
from app.core.enums import EventType, DetentionCaseStatus
from app.services.rules_engine import resolve_ruleset_for_stop
from app.services.detention_math import compute_detention_metrics


def _get_event_time(stop: Stop, event_type: EventType) -> datetime | None:
    for event in stop.events:
        if event.event_type == event_type:
            return event.occurred_at
    return None


def recompute_detention_case_for_stop(db: Session, stop_id: int) -> DetentionCase | None:
    stop = (
        db.query(Stop)
        .options(
            joinedload(Stop.load),
            joinedload(Stop.events),
            joinedload(Stop.detention_case),
        )
        .filter(Stop.id == stop_id)
        .first()
    )
    if not stop:
        return None

    arrived_at = _get_event_time(stop, EventType.arrived)
    departed_at = _get_event_time(stop, EventType.departed)

    if not arrived_at:
        return stop.detention_case

    ruleset = resolve_ruleset_for_stop(
        db=db,
        organization_id=stop.organization_id,
        facility_id=stop.facility_id,
        customer_name=stop.load.customer_name if stop.load else None,
        reference_time=arrived_at,
    )
    if not ruleset:
        return stop.detention_case

    dwell_minutes = 0
    if departed_at:
        dwell_minutes = max(int((departed_at - arrived_at).total_seconds() // 60), 0)

    metrics = compute_detention_metrics(
        dwell_minutes=dwell_minutes,
        free_minutes=ruleset.free_minutes,
        grace_minutes=ruleset.grace_minutes,
        billable_unit_minutes=ruleset.billable_unit_minutes,
        rate_per_unit=ruleset.rate_per_unit,
    )

    detention_case = stop.detention_case
    if detention_case is None:
        detention_case = DetentionCase(
            organization_id=stop.organization_id,
            load_id=stop.load_id,
            stop_id=stop.id,
        )
        db.add(detention_case)

    detention_case.ruleset_id = ruleset.id
    detention_case.status = (
        DetentionCaseStatus.closed if departed_at else DetentionCaseStatus.open
    )
    detention_case.eligible_at = arrived_at
    detention_case.closed_at = departed_at
    detention_case.last_computed_at = datetime.utcnow()
    detention_case.free_minutes_applied = ruleset.free_minutes
    detention_case.grace_minutes_applied = ruleset.grace_minutes
    detention_case.billable_unit_minutes_applied = ruleset.billable_unit_minutes
    detention_case.dwell_minutes = metrics["dwell_minutes"]
    detention_case.billable_minutes = metrics["billable_minutes"]
    detention_case.billable_units = metrics["billable_units"]
    detention_case.rate_per_unit_snapshot = ruleset.rate_per_unit
    detention_case.amount = metrics["amount"]
    detention_case.currency = ruleset.currency

    db.flush()
    return detention_case
