from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db
from app.models.event import Event

router = APIRouter(
    tags=["Analytics"]
)


@router.get("/analytics/visitors")
def visitor_analytics(
    db: Session = Depends(get_db)
):

    unique_visitors = (
        db.query(
            func.count(
                func.distinct(Event.visitor_id)
            )
        )
        .scalar()
    )

    visitor_counts = (
        db.query(
            Event.visitor_id,
            func.count(Event.visitor_id)
        )
        .group_by(Event.visitor_id)
        .all()
    )

    repeat_visitors = sum(
        1
        for _, count in visitor_counts
        if count > 1
    )

    repeat_rate = (
        repeat_visitors / unique_visitors
        if unique_visitors > 0
        else 0
    )

    return {
        "unique_visitors": unique_visitors,
        "repeat_visitors": repeat_visitors,
        "repeat_rate": round(
            repeat_rate,
            4
        )
    }