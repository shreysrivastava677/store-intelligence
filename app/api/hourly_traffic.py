from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database.dependencies import get_db
from app.models.event import Event

router = APIRouter(
    tags=["Analytics"]
)


@router.get("/analytics/hourly-traffic")
def hourly_traffic(
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            extract("hour", Event.timestamp).label("hour"),
            func.count(Event.event_id).label("event_count")
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    traffic = []

    for hour, count in results:

        traffic.append(
            {
                "hour": int(hour),
                "event_count": count
            }
        )

    return {
        "hourly_traffic": traffic
    }