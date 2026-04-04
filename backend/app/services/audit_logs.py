from sqlalchemy.orm import Session

from app.core.enums import AuditAction
from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    *,
    organization_id: int,
    action: AuditAction,
    load_id: int | None = None,
    stop_id: int | None = None,
    detention_case_id: int | None = None,
    created_by_user_id: int | None = None,
    message: str | None = None,
    payload_json: dict | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        organization_id=organization_id,
        load_id=load_id,
        stop_id=stop_id,
        detention_case_id=detention_case_id,
        created_by_user_id=created_by_user_id,
        action=action,
        message=message,
        payload_json=payload_json,
    )
    db.add(audit_log)
    db.flush()
    return audit_log
