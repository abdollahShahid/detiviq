from app.schemas.common import TimestampedSchema
from pydantic import BaseModel


class FacilityCreate(BaseModel):
    name: str
    code: str | None = None
    customer_name: str | None = None
    timezone: str = "UTC"
    city: str | None = None
    state: str | None = None


class FacilityRead(TimestampedSchema):
    organization_id: int
    name: str
    code: str | None = None
    customer_name: str | None = None
    timezone: str
    city: str | None = None
    state: str | None = None
    is_active: bool
