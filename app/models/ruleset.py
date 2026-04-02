from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import RulesetScope
from app.db.session import Base
from app.models.mixins import TimestampMixin


class Ruleset(TimestampMixin, Base):
    __tablename__ = "rulesets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope_type: Mapped[RulesetScope] = mapped_column(
        SqlEnum(RulesetScope, name="ruleset_scope"), nullable=False
    )
    facility_id: Mapped[int | None] = mapped_column(ForeignKey("facilities.id"), nullable=True)
    customer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    free_minutes: Mapped[int] = mapped_column(nullable=False)
    grace_minutes: Mapped[int] = mapped_column(default=0, nullable=False)
    billable_unit_minutes: Mapped[int] = mapped_column(default=60, nullable=False)
    rate_per_unit: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    effective_from: Mapped[datetime | None] = mapped_column(nullable=True)
    effective_to: Mapped[datetime | None] = mapped_column(nullable=True)
    priority: Mapped[int] = mapped_column(default=100, nullable=False)

    organization = relationship("Organization", back_populates="rulesets")
    facility = relationship("Facility", back_populates="rulesets")
