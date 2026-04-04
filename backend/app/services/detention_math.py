from decimal import Decimal, ROUND_HALF_UP


def round_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ceil_div(value: int, unit: int) -> int:
    if unit <= 0:
        raise ValueError("billable unit must be greater than zero")
    if value <= 0:
        return 0
    return (value + unit - 1) // unit


def compute_detention_metrics(
    dwell_minutes: int,
    free_minutes: int,
    grace_minutes: int,
    billable_unit_minutes: int,
    rate_per_unit: Decimal,
) -> dict:
    chargeable_after_free = max(dwell_minutes - free_minutes, 0)
    chargeable_after_grace = max(chargeable_after_free - grace_minutes, 0)

    billable_units = ceil_div(chargeable_after_grace, billable_unit_minutes)
    amount = round_money(Decimal(billable_units) * rate_per_unit)

    return {
        "dwell_minutes": max(dwell_minutes, 0),
        "billable_minutes": chargeable_after_grace,
        "billable_units": billable_units,
        "amount": amount,
    }
