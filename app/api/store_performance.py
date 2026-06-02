from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db
from app.models.event import Event

router = APIRouter(
    tags=["Analytics"]
)


@router.get("/analytics/store-performance")
def store_performance(
    db: Session = Depends(get_db)
):

    stores = (
        db.query(Event.store_id)
        .distinct()
        .all()
    )

    performance = []

    for (store_id,) in stores:

        total_events = (
            db.query(Event)
            .filter(
                Event.store_id == store_id
            )
            .count()
        )

        unique_visitors = (
            db.query(
                func.count(
                    func.distinct(
                        Event.visitor_id
                    )
                )
            )
            .filter(
                Event.store_id == store_id
            )
            .scalar()
        )

        entries = (
            db.query(Event)
            .filter(
                Event.store_id == store_id,
                Event.event_type == "ENTRY"
            )
            .count()
        )

        purchases = (
            db.query(Event)
            .filter(
                Event.store_id == store_id,
                Event.event_type == "PURCHASE"
            )
            .count()
        )

        conversion_rate = (
            purchases / entries
            if entries > 0
            else 0
        )

        performance.append(
            {
                "store_id": store_id,
                "total_events": total_events,
                "unique_visitors": unique_visitors,
                "entries": entries,
                "purchases": purchases,
                "conversion_rate": round(
                    conversion_rate,
                    4
                )
            }
        )

    return {
        "stores": performance
    }