from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import DetentionCaseStatus
from app.db.session import Base
from app.models.mixins import TimestampMixin


class DetentionCase(TimestampMixin, Base):
    __tablename__ = "detention_cases"
    __table_args__ = (
        UniqueConstraint("stop_id", name="uq_detention_case_stop_id"),
        Index("ix_detention_case_org_status", "organization_id", "status"),
        Index("ix_detention_case_load_id", "load_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id"), nullable=False)
    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.id"), nullable=False)
    ruleset_id: Mapped[int | None] = mapped_column(ForeignKey("rulesets.id"), nullable=True)

    status: Mapped[DetentionCaseStatus] = mapped_column(
        SqlEnum(DetentionCaseStatus, name="detention_case_status"),
        default=DetentionCaseStatus.open,
        nullable=False,
    )

    eligible_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_computed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    free_minutes_applied: Mapped[int] = mapped_column(default=0, nullable=False)
    grace_minutes_applied: Mapped[int] = mapped_column(default=0, nullable=False)
    billable_unit_minutes_applied: Mapped[int] = mapped_column(default=60, nullable=False)

    dwell_minutes: Mapped[int] = mapped_column(default=0, nullable=False)
    billable_minutes: Mapped[int] = mapped_column(default=0, nullable=False)
    billable_units: Mapped[int] = mapped_column(default=0, nullable=False)

    rate_per_unit_snapshot: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)

    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    organization = relationship("Organization", back_populates="detention_cases")
    load = relationship("Load", back_populates="detention_cases")
    stop = relationship("Stop", back_populates="detention_case")
    ruleset = relationship("Ruleset", back_populates="detention_cases")
