import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest_idempotency():

    event_id = str(
        uuid.uuid4()
    )

    payload = {
        "events": [
            {
                "event_id": event_id,
                "visitor_id": "test_user",
                "store_id": "store_1",
                "camera_id": "camera_1",
                "event_type": "ENTRY",
                "confidence": 0.95,
                "timestamp": "2026-06-02T10:00:00Z",
                "metadata": {}
            }
        ]
    }

    first = client.post(
        "/events/ingest",
        json=payload
    )

    second = client.post(
        "/events/ingest",
        json=payload
    )

    assert first.status_code == 200
    assert second.status_code == 200

    second_data = second.json()

    assert len(
        second_data["duplicates"]
    ) == 1