from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.enums import RulesetScope
from app.models.ruleset import Ruleset


def resolve_ruleset_for_stop(
    db: Session,
    organization_id: int,
    facility_id: int | None,
    customer_name: str | None,
    reference_time: datetime | None = None,
) -> Ruleset | None:
    query = db.query(Ruleset).filter(
        Ruleset.organization_id == organization_id,
        Ruleset.is_active.is_(True),
    )

    if reference_time is not None:
        query = query.filter(
            or_(Ruleset.effective_from.is_(None), Ruleset.effective_from <= reference_time),
            or_(Ruleset.effective_to.is_(None), Ruleset.effective_to >= reference_time),
        )

    facility_rule = None
    if facility_id is not None:
        facility_rule = (
            query.filter(
                Ruleset.scope_type == RulesetScope.facility,
                Ruleset.facility_id == facility_id,
            )
            .order_by(Ruleset.priority.asc(), Ruleset.id.asc())
            .first()
        )
    if facility_rule:
        return facility_rule

    customer_rule = None
    if customer_name:
        customer_rule = (
            query.filter(
                Ruleset.scope_type == RulesetScope.customer,
                Ruleset.customer_name == customer_name,
            )
            .order_by(Ruleset.priority.asc(), Ruleset.id.asc())
            .first()
        )
    if customer_rule:
        return customer_rule

    return (
        query.filter(Ruleset.scope_type == RulesetScope.organization_default)
        .order_by(Ruleset.priority.asc(), Ruleset.id.asc())
        .first()
    )
