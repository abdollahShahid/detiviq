from datetime import datetime
from decimal import Decimal

from app.core.enums import RulesetScope
from app.schemas.common import TimestampedSchema
from pydantic import BaseModel


class RulesetCreate(BaseModel):
    name: str
    scope_type: RulesetScope
    facility_id: int | None = None
    customer_name: str | None = None
    free_minutes: int
    grace_minutes: int = 0
    billable_unit_minutes: int = 60
    rate_per_unit: Decimal
    currency: str = "USD"
    is_active: bool = True
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    priority: int = 100


class RulesetRead(TimestampedSchema):
    organization_id: int
    name: str
    scope_type: RulesetScope
    facility_id: int | None = None
    customer_name: str | None = None
    free_minutes: int
    grace_minutes: int
    billable_unit_minutes: int
    rate_per_unit: Decimal
    currency: str
    is_active: bool
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    priority: int
