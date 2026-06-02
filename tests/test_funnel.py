from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_funnel():

    response = client.get(
        "/analytics/funnel"
    )

    assert response.status_code == 200

    data = response.json()

    assert "funnel" in data
    assert "conversion_rates" in data