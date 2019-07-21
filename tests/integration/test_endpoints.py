import json


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_number_echo(client):
    response = client.post("/number_echo", data=json.dumps({"number": 42}))
    assert response.status_code == 200

    # first point is never assigned to a cluster
    assert response.json()["number"] == 42
