from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:

    @staticmethod
    def exists(
        db: Session,
        event_id
    ):
        return (
            db.query(Event)
            .filter(Event.event_id == event_id)
            .first()
            is not None
        )

    @staticmethod
    def create(
        db: Session,
        event: Event
    ):
        db.add(event)

        db.commit()

        db.refresh(event)

        return event