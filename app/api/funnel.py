from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.event import Event

router = APIRouter(
    tags=["Analytics"]
)


@router.get(
    "/analytics/funnel"
)
def funnel(
    db: Session = Depends(get_db)
):

    entry_visitors = set(
        row[0]
        for row in (
            db.query(
                Event.visitor_id
            )
            .filter(
                Event.event_type == "ENTRY"
            )
            .distinct()
            .all()
        )
    )

    zone_visitors = set(
        row[0]
        for row in (
            db.query(
                Event.visitor_id
            )
            .filter(
                Event.event_type == "ZONE_VISIT"
            )
            .distinct()
            .all()
        )
    )

    billing_visitors = set(
        row[0]
        for row in (
            db.query(
                Event.visitor_id
            )
            .filter(
                Event.event_type == "BILLING_QUEUE"
            )
            .distinct()
            .all()
        )
    )

    purchase_visitors = set(
        row[0]
        for row in (
            db.query(
                Event.visitor_id
            )
            .filter(
                Event.event_type == "PURCHASE"
            )
            .distinct()
            .all()
        )
    )

    entries = len(
        entry_visitors
    )

    zone_visits = len(
        zone_visitors
    )

    billing = len(
        billing_visitors
    )

    purchases = len(
        purchase_visitors
    )

    zone_conversion = (
        round(
            (zone_visits / entries) * 100,
            2
        )
        if entries > 0
        else 0
    )

    billing_conversion = (
        round(
            (billing / zone_visits) * 100,
            2
        )
        if zone_visits > 0
        else 0
    )

    purchase_conversion = (
        round(
            (purchases / billing) * 100,
            2
        )
        if billing > 0
        else 0
    )

    overall_conversion = (
        round(
            (purchases / entries) * 100,
            2
        )
        if entries > 0
        else 0
    )

    return {
        "funnel": {
            "entry": entries,
            "zone_visit": zone_visits,
            "billing_queue": billing,
            "purchase": purchases
        },
        "conversion_rates": {
            "entry_to_zone":
                zone_conversion,
            "zone_to_billing":
                billing_conversion,
            "billing_to_purchase":
                purchase_conversion,
            "overall":
                overall_conversion
        }
    }