from datetime import datetime

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import LoadStatus
from app.db.session import Base
from app.models.mixins import TimestampMixin


class Load(TimestampMixin, Base):
    __tablename__ = "loads"
    __table_args__ = (
        UniqueConstraint("organization_id", "external_reference", name="uq_load_org_external_reference"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    external_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[LoadStatus] = mapped_column(
        SqlEnum(LoadStatus, name="load_status"), default=LoadStatus.planned, nullable=False
    )
    origin_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    destination_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scheduled_pickup_at: Mapped[datetime | None] = mapped_column(nullable=True)
    scheduled_delivery_at: Mapped[datetime | None] = mapped_column(nullable=True)

    organization = relationship("Organization", back_populates="loads")
    created_by_user = relationship("User", back_populates="created_loads")
    stops = relationship("Stop", back_populates="load", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="load", order_by="Event.occurred_at")
    events = relationship("Event", back_populates="load", order_by="Event.occurred_at")



