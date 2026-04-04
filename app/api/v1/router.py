from fastapi import APIRouter

from app.api.v1.endpoints import (
    analytics,
    auth,
    detention_cases,
    events,
    facilities,
    loads,
    rulesets,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(facilities.router, prefix="/facilities", tags=["facilities"])
api_router.include_router(loads.router, prefix="/loads", tags=["loads"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(rulesets.router, prefix="/rulesets", tags=["rulesets"])
api_router.include_router(detention_cases.router, prefix="/detention-cases", tags=["detention-cases"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
