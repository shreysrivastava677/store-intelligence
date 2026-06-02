from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(
    tags=["Heatmap"]
)


@router.get(
    "/stores/{store_id}/heatmap"
)
def heatmap(store_id: int):

    db = SessionLocal()

    try:

        results = db.execute(
            text("""
                SELECT
                    event_metadata->>'zone' AS zone,
                    COUNT(*) AS visit_frequency,
                    COUNT(DISTINCT visitor_id) AS unique_visitors
                FROM events
                WHERE event_type='ZONE_VISIT'
                GROUP BY zone
            """)
        )

        rows = list(results)

        if not rows:

            return {
                "store_id": store_id,
                "heatmap": {}
            }

        max_visits = max(
            row.visit_frequency
            for row in rows
        )

        response = {}

        for row in rows:

            score = int(
                (
                    row.visit_frequency
                    / max_visits
                ) * 100
            )

            confidence = (
                "HIGH"
                if row.unique_visitors >= 20
                else "LOW"
            )

            response[row.zone] = {
                "visit_frequency":
                    row.visit_frequency,
                "unique_visitors":
                    row.unique_visitors,
                "score":
                    score,
                "data_confidence":
                    confidence
            }

        return {
            "store_id": store_id,
            "heatmap": response
        }

    finally:

        db.close()