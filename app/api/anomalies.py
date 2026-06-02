from fastapi import APIRouter
from sqlalchemy import text

from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.database.session import SessionLocal

from app.logger import logger

router = APIRouter(
    tags=["Anomalies"]
)


@router.get(
    "/stores/{store_id}/anomalies"
)
def get_anomalies(store_id: int):

    db = SessionLocal()

    anomalies = []

    try:

        dead_zones = db.execute(
            text("""
                SELECT
                    event_metadata->>'zone' AS zone,
                    MAX(timestamp) AS last_visit
                FROM events
                WHERE event_type='ZONE_VISIT'
                GROUP BY zone
            """)
        )

        now = datetime.now(
            timezone.utc
        )

        for row in dead_zones:

            if row.last_visit:

                last_visit = row.last_visit

                if last_visit.tzinfo is None:

                    last_visit = (
                        last_visit.replace(
                            tzinfo=timezone.utc
                        )
                    )

                diff = now - last_visit

                if diff > timedelta(
                    minutes=30
                ):

                    anomalies.append(
                        {
                            "type":
                                "DEAD_ZONE",

                            "severity":
                                "WARN",

                            "zone":
                                row.zone,

                            "description":
                                f"No visits detected in "
                                f"{row.zone} for 30+ minutes",

                            "suggested_action":
                                "Review product placement "
                                "or promotions"
                        }
                    )

        visitors = db.execute(
            text("""
                SELECT COUNT(
                    DISTINCT visitor_id
                )
                FROM events
                WHERE event_type='ZONE_VISIT'
            """)
        ).scalar()

        if visitors < 5:

            anomalies.append(
                {
                    "type":
                        "LOW_TRAFFIC",

                    "severity":
                        "INFO",

                    "description":
                        "Store traffic below "
                        "expected threshold",

                    "suggested_action":
                        "Review marketing campaigns"
                }
            )

        total_events = db.execute(
            text("""
                SELECT COUNT(*)
                FROM events
                WHERE event_type='ZONE_VISIT'
            """)
        ).scalar()

        if total_events > 500:

            anomalies.append(
                {
                    "type":
                        "QUEUE_SPIKE",

                    "severity":
                        "CRITICAL",

                    "description":
                        "Abnormally high visitor "
                        "activity detected",

                    "suggested_action":
                        "Deploy additional staff"
                }
            )

        logger.info(
            {
                "store_id":
                    store_id,

                "anomaly_count":
                    len(anomalies)
            }
        )

        return {
            "store_id":
                store_id,

            "anomaly_count":
                len(anomalies),

            "anomalies":
                anomalies
        }

    finally:

        db.close()