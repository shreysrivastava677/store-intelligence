from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_heatmap():

    response = client.get(
        "/stores/1/heatmap"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        dict
    )