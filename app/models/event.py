from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EventType
from app.db.session import Base
from app.models.mixins import TimestampMixin


class Event(TimestampMixin, Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id"), nullable=False)
    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.id"), nullable=False)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType, name="event_type"), nullable=False)
    occurred_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="api", nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payload_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ingested_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    load = relationship("Load", back_populates="events")
    stop = relationship("Stop", back_populates="events")

    __table_args__ = (
        Index("ix_event_stop_occurred_at", "stop_id", "occurred_at"),
        Index("ix_event_load_occurred_at", "load_id", "occurred_at"),
        UniqueConstraint("organization_id", "idempotency_key", name="uq_event_org_idempotency_key"),
    )
