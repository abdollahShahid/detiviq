from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class Facility(TimestampMixin, Base):
    __tablename__ = "facilities"
    __table_args__ = (
        UniqueConstraint("organization_id", "name", name="uq_facility_org_name"),
        Index("ix_facility_org_customer", "organization_id", "customer_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    customer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timezone: Mapped[str] = mapped_column(String(100), default="UTC", nullable=False)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    organization = relationship("Organization", back_populates="facilities")
    stops = relationship("Stop", back_populates="facility")
    rulesets = relationship("Ruleset", back_populates="facility")
