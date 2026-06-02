from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.event import Event

from app.repositories.event_repository import (
    EventRepository
)

from app.schemas.event import (
    EventBatchRequest,
    IngestionResponse
)

from app.logger import logger

router = APIRouter(
    tags=["Event Ingestion"]
)


@router.post(
    "/events/ingest",
    response_model=IngestionResponse
)
def ingest_events(
    payload: EventBatchRequest,
    db: Session = Depends(get_db)
):

    if len(payload.events) > 500:

        raise HTTPException(
            status_code=400,
            detail="Maximum 500 events per request"
        )

    accepted = []
    duplicates = []
    failed = []

    for event in payload.events:

        try:

            # Idempotency Check

            if EventRepository.exists(
                db,
                event.event_id
            ):

                duplicates.append(
                    str(event.event_id)
                )

                logger.warning(
                    {
                        "event_id":
                            str(event.event_id),
                        "status":
                            "duplicate"
                    }
                )

                continue

            db_event = Event(
                event_id=event.event_id,
                visitor_id=event.visitor_id,
                store_id=event.store_id,
                camera_id=event.camera_id,
                event_type=event.event_type,
                confidence=event.confidence,
                timestamp=event.timestamp,
                event_metadata=event.metadata
            )

            EventRepository.create(
                db,
                db_event
            )

            accepted.append(
                str(event.event_id)
            )

            logger.info(
                {
                    "event_id":
                        str(event.event_id),

                    "visitor_id":
                        event.visitor_id,

                    "event_type":
                        event.event_type,

                    "status":
                        "accepted"
                }
            )

        except Exception as exc:

            failed.append(
                {
                    "event_id":
                        str(event.event_id),

                    "error":
                        str(exc)
                }
            )

            logger.error(
                {
                    "event_id":
                        str(event.event_id),

                    "error":
                        str(exc)
                }
            )

    return {
        "summary": {
            "received":
                len(payload.events),

            "accepted":
                len(accepted),

            "duplicates":
                len(duplicates),

            "failed":
                len(failed)
        },

        "accepted":
            accepted,

        "duplicates":
            duplicates,

        "failed":
            failed
    }