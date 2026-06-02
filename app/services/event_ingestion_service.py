from uuid import uuid4
from datetime import datetime

from app.models.event import Event


class EventIngestionService:

    @staticmethod
    def save_event(
        db,
        visitor_id,
        zone,
        event_type
    ):

        event = Event(
            event_id=uuid4(),
            visitor_id=str(visitor_id),
            store_id="store_1",
            camera_id="cam_1",
            event_type=event_type,
            confidence=1.0,
            timestamp=datetime.utcnow(),
            event_metadata={
                "zone": zone
            }
        )

        db.add(event)
        db.commit()