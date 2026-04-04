from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.core.enums import DetentionCaseStatus
from app.db.deps import get_db
from app.models.detention_case import DetentionCase
from app.models.facility import Facility
from app.models.stop import Stop
from app.schemas.analytics import (
    OpenDetentionCasesSummary,
    RevenueLossSummary,
    TopDelayedFacilityRow,
)

router = APIRouter()


@router.get("/open-detention-cases-summary", response_model=OpenDetentionCasesSummary)
def get_open_detention_cases_summary(db: Session = Depends(get_db)):
    result = (
        db.query(
            func.count(DetentionCase.id).label("open_case_count"),
            func.sum(DetentionCase.amount).label("total_open_amount"),
            func.avg(DetentionCase.amount).label("avg_open_amount"),
        )
        .filter(
            DetentionCase.organization_id == 1,
            DetentionCase.status == DetentionCaseStatus.open,
        )
        .one()
    )

    return {
        "open_case_count": result.open_case_count or 0,
        "total_open_amount": result.total_open_amount or Decimal("0.00"),
        "avg_open_amount": result.avg_open_amount or Decimal("0.00"),
    }


@router.get("/top-delayed-facilities", response_model=list[TopDelayedFacilityRow])
def get_top_delayed_facilities(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Facility.id.label("facility_id"),
            Facility.name.label("facility_name"),
            func.count(DetentionCase.id).label("stop_count"),
            func.avg(DetentionCase.dwell_minutes).label("avg_dwell_minutes"),
            func.sum(DetentionCase.amount).label("total_amount"),
        )
        .join(Stop, Stop.facility_id == Facility.id)
        .join(DetentionCase, DetentionCase.stop_id == Stop.id)
        .filter(
            Facility.organization_id == 1,
            DetentionCase.dwell_minutes.isnot(None),
        )
        .group_by(Facility.id, Facility.name)
        .order_by(
            func.avg(DetentionCase.dwell_minutes).desc(),
            func.sum(DetentionCase.amount).desc(),
        )
        .limit(5)
        .all()
    )

    return [
        {
            "facility_id": row.facility_id,
            "facility_name": row.facility_name,
            "stop_count": row.stop_count or 0,
            "avg_dwell_minutes": row.avg_dwell_minutes or Decimal("0.00"),
            "total_amount": row.total_amount or Decimal("0.00"),
        }
        for row in rows
    ]


@router.get("/revenue-loss-summary", response_model=RevenueLossSummary)
def get_revenue_loss_summary(db: Session = Depends(get_db)):
    result = (
        db.query(
            func.count(DetentionCase.id).label("total_cases"),
            func.sum(DetentionCase.amount).label("total_amount"),
            func.avg(DetentionCase.amount).label("avg_amount"),
            func.sum(
                case((DetentionCase.status == DetentionCaseStatus.closed, 1), else_=0)
            ).label("closed_case_count"),
            func.sum(
                case((DetentionCase.status == DetentionCaseStatus.open, 1), else_=0)
            ).label("open_case_count"),
        )
        .filter(DetentionCase.organization_id == 1)
        .one()
    )

    return {
        "total_cases": result.total_cases or 0,
        "total_amount": result.total_amount or Decimal("0.00"),
        "avg_amount": result.avg_amount or Decimal("0.00"),
        "closed_case_count": result.closed_case_count or 0,
        "open_case_count": result.open_case_count or 0,
    }
