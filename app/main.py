from datetime import (
    datetime,
    timedelta,
    timezone
)

from fastapi import (
    FastAPI,
    Request
)

from sqlalchemy import text

from app.database.session import SessionLocal

from app.middleware.logging_middleware import (
    logging_middleware
)

from app.api.ingest import (
    router as ingest_router
)

from app.api.analytics import (
    router as analytics_router
)

from app.api.funnel import (
    router as funnel_router
)

from app.api.visitors import (
    router as visitors_router
)

from app.api.hourly_traffic import (
    router as hourly_traffic_router
)

from app.api.store_performance import (
    router as store_performance_router
)

from app.api.zone_performance import (
    router as zone_performance_router
)

from app.api.anomalies import (
    router as anomalies_router
)

from app.api.heatmap import (
    router as heatmap_router
)

app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0",
    description="Retail Store Intelligence Platform"
)


@app.middleware("http")
async def request_logger(
    request: Request,
    call_next
):
    return await logging_middleware(
        request,
        call_next
    )


# Register Routers

app.include_router(
    ingest_router
)

app.include_router(
    analytics_router
)

app.include_router(
    funnel_router
)

app.include_router(
    visitors_router
)

app.include_router(
    hourly_traffic_router
)

app.include_router(
    store_performance_router
)

app.include_router(
    zone_performance_router
)

app.include_router(
    anomalies_router
)

app.include_router(
    heatmap_router
)


@app.get("/")
def root():

    return {
        "message": "Store Intelligence API Running"
    }


@app.get("/health")
def health():

    db = SessionLocal()

    try:

        latest_event = db.execute(
            text("""
                SELECT MAX(timestamp)
                FROM events
            """)
        ).scalar()

        total_events = db.execute(
            text("""
                SELECT COUNT(*)
                FROM events
            """)
        ).scalar()

        stale_feed = False

        if latest_event:

            if latest_event.tzinfo is None:

                latest_event = (
                    latest_event.replace(
                        tzinfo=timezone.utc
                    )
                )

            stale_feed = (
                datetime.now(
                    timezone.utc
                ) - latest_event
            ) > timedelta(
                minutes=30
            )

        return {
            "service":
                "store-intelligence",

            "status":
                "healthy",

            "last_event_timestamp":
                latest_event,

            "stale_feed":
                stale_feed,

            "total_events":
                total_events
        }

    finally:

        db.close()