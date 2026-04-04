from datetime import datetime
from decimal import Decimal

from app.core.enums import DetentionCaseStatus
from app.schemas.common import TimestampedSchema


class DetentionCaseRead(TimestampedSchema):
    organization_id: int
    load_id: int
    stop_id: int
    ruleset_id: int | None = None
    status: DetentionCaseStatus
    eligible_at: datetime | None = None
    closed_at: datetime | None = None
    last_computed_at: datetime | None = None
    free_minutes_applied: int
    grace_minutes_applied: int
    billable_unit_minutes_applied: int
    dwell_minutes: int
    billable_minutes: int
    billable_units: int
    rate_per_unit_snapshot: Decimal
    amount: Decimal
    currency: str
    notes: str | None = None
