from decimal import Decimal

from app.schemas.common import ORMModel


class OpenDetentionCasesSummary(ORMModel):
    open_case_count: int
    total_open_amount: Decimal
    avg_open_amount: Decimal


class TopDelayedFacilityRow(ORMModel):
    facility_id: int
    facility_name: str
    stop_count: int
    avg_dwell_minutes: Decimal
    total_amount: Decimal


class RevenueLossSummary(ORMModel):
    total_cases: int
    total_amount: Decimal
    avg_amount: Decimal
    closed_case_count: int
    open_case_count: int
