from uuid import UUID
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


class EventSchema(BaseModel):

    event_id: UUID

    visitor_id: str

    store_id: str

    camera_id: str

    event_type: str

    confidence: float = Field(
        ge=0,
        le=1
    )

    timestamp: datetime

    metadata: dict = {}

    model_config = ConfigDict(
        from_attributes=True
    )


class EventBatchRequest(BaseModel):

    events: list[EventSchema]


class IngestionSummary(BaseModel):

    received: int

    accepted: int

    duplicates: int

    failed: int


class IngestionResponse(BaseModel):

    summary: IngestionSummary

    accepted: list[str]

    duplicates: list[str]

    failed: list[dict]