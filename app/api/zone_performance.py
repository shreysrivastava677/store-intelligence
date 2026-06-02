from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(
    tags=["Zone Performance"]
)


@router.get(
    "/analytics/zone-performance"
)
def zone_performance():

    db = SessionLocal()

    try:

        results = db.execute(
            text("""
                SELECT
                    event_metadata->>'zone' AS zone,
                    COUNT(*) AS total_visits,
                    COUNT(DISTINCT visitor_id) AS unique_visitors
                FROM events
                WHERE event_type = 'ZONE_VISIT'
                GROUP BY zone
                ORDER BY total_visits DESC
            """)
        )

        response = {}

        for row in results:

            response[row.zone] = {
                "total_visits": row.total_visits,
                "unique_visitors": row.unique_visitors
            }

        return response

    finally:

        db.close()


@router.get(
    "/analytics/zone-summary"
)
def zone_summary():

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT
                    COUNT(DISTINCT visitor_id) AS visitors,
                    COUNT(*) AS events
                FROM events
                WHERE event_type='ZONE_VISIT'
            """)
        ).first()

        return {
            "total_zone_events": result.events,
            "unique_visitors": result.visitors
        }

    finally:

        db.close()