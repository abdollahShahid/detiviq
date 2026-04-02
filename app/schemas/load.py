from datetime import datetime

from app.core.enums import LoadStatus
from app.schemas.common import TimestampedSchema
from pydantic import BaseModel


class LoadCreate(BaseModel):
    external_reference: str
    customer_name: str
    origin_label: str | None = None
    destination_label: str | None = None
    scheduled_pickup_at: datetime | None = None
    scheduled_delivery_at: datetime | None = None


class LoadRead(TimestampedSchema):
    organization_id: int
    created_by_user_id: int | None = None
    external_reference: str
    customer_name: str
    status: LoadStatus
    origin_label: str | None = None
    destination_label: str | None = None
    scheduled_pickup_at: datetime | None = None
    scheduled_delivery_at: datetime | None = None
