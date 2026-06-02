from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    DateTime,
    JSON
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class Event(Base):
    """
    Immutable event store.
    Core table powering all analytics.
    """

    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    visitor_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True
    )

    store_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True
    )

    camera_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    event_metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )