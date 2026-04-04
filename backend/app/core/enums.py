import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    dispatcher = "dispatcher"
    analyst = "analyst"


class LoadStatus(str, enum.Enum):
    planned = "planned"
    in_transit = "in_transit"
    completed = "completed"
    cancelled = "cancelled"


class StopType(str, enum.Enum):
    pickup = "pickup"
    delivery = "delivery"


class StopStatus(str, enum.Enum):
    planned = "planned"
    arrived = "arrived"
    loading = "loading"
    departed = "departed"
    completed = "completed"


class EventType(str, enum.Enum):
    arrived = "arrived"
    checked_in = "checked_in"
    loading_started = "loading_started"
    loading_finished = "loading_finished"
    departed = "departed"


class RulesetScope(str, enum.Enum):
    facility = "facility"
    customer = "customer"
    organization_default = "organization_default"

class DetentionCaseStatus(str, enum.Enum):
    open = "open"
    closed = "closed"

class AuditAction(str, enum.Enum):
    detention_case_computed = "detention_case_computed"
    detention_case_closed = "detention_case_closed"
