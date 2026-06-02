from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db
from app.models.event import Event

router = APIRouter(
    tags=["Analytics"]
)


@router.get("/analytics/metrics")
def metrics(
    db: Session = Depends(get_db)
):

    total_events = db.query(Event).count()

    unique_visitors = (
        db.query(
            func.count(
                func.distinct(
                    Event.visitor_id
                )
            )
        )
        .scalar()
    )

    entries = (
        db.query(Event)
        .filter(
            Event.event_type == "ENTRY"
        )
        .count()
    )

    purchases = (
        db.query(Event)
        .filter(
            Event.event_type == "PURCHASE"
        )
        .count()
    )

    conversion_rate = (
        purchases / entries
        if entries > 0
        else 0
    )

    return {
        "total_events": total_events,
        "unique_visitors": unique_visitors,
        "entries": entries,
        "purchases": purchases,
        "conversion_rate": round(
            conversion_rate,
            4
        )
    }