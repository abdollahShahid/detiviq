from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AuditAction
from app.db.session import Base
from app.models.mixins import TimestampMixin


class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    load_id: Mapped[int | None] = mapped_column(ForeignKey("loads.id"), nullable=True)
    stop_id: Mapped[int | None] = mapped_column(ForeignKey("stops.id"), nullable=True)
    detention_case_id: Mapped[int | None] = mapped_column(ForeignKey("detention_cases.id"), nullable=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    action: Mapped[AuditAction] = mapped_column(
        SqlEnum(AuditAction, name="audit_action"), nullable=False
    )
    message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payload_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    organization = relationship("Organization")
    load = relationship("Load")
    stop = relationship("Stop")
    detention_case = relationship("DetentionCase")
    created_by_user = relationship("User")
