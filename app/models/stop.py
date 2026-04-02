from datetime import datetime

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import StopStatus, StopType
from app.db.session import Base
from app.models.mixins import TimestampMixin


class Stop(TimestampMixin, Base):
    __tablename__ = "stops"
    __table_args__ = (
        UniqueConstraint("load_id", "stop_number", name="uq_stop_load_stop_number"),
        Index("ix_stop_load_stop_number", "load_id", "stop_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id"), nullable=False)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"), nullable=False)
    stop_number: Mapped[int] = mapped_column(nullable=False)
    stop_type: Mapped[StopType] = mapped_column(
        SqlEnum(StopType, name="stop_type"), nullable=False
    )
    status: Mapped[StopStatus] = mapped_column(
        SqlEnum(StopStatus, name="stop_status"), default=StopStatus.planned, nullable=False
    )
    appointment_at: Mapped[datetime | None] = mapped_column(nullable=True)
    actual_arrived_at: Mapped[datetime | None] = mapped_column(nullable=True)
    actual_departed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    current_dwell_minutes: Mapped[int] = mapped_column(default=0, nullable=False)

    load = relationship("Load", back_populates="stops")
    facility = relationship("Facility", back_populates="stops")
