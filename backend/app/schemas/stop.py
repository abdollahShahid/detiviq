from datetime import datetime

from app.core.enums import StopStatus, StopType
from app.schemas.common import TimestampedSchema
from pydantic import BaseModel


class StopCreate(BaseModel):
    facility_id: int
    stop_number: int
    stop_type: StopType
    appointment_at: datetime | None = None


class StopRead(TimestampedSchema):
    organization_id: int
    load_id: int
    facility_id: int
    stop_number: int
    stop_type: StopType
    status: StopStatus
    appointment_at: datetime | None = None
    actual_arrived_at: datetime | None = None
    actual_departed_at: datetime | None = None
    current_dwell_minutes: int
