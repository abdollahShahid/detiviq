from datetime import datetime

from pydantic import BaseModel

from app.core.enums import EventType
from app.schemas.common import TimestampedSchema


class EventCreate(BaseModel):
    load_id: int
    stop_id: int
    event_type: EventType
    occurred_at: datetime
    source: str = "api"
    idempotency_key: str | None = None
    payload_json: dict | None = None


class EventRead(TimestampedSchema):
    organization_id: int
    load_id: int
    stop_id: int
    event_type: EventType
    occurred_at: datetime
    source: str
    idempotency_key: str | None = None
    payload_json: dict | None = None
    ingested_by_user_id: int | None = None
