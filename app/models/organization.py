from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    users = relationship("User", back_populates="organization")
    facilities = relationship("Facility", back_populates="organization")
    loads = relationship("Load", back_populates="organization")
    rulesets = relationship("Ruleset", back_populates="organization")
