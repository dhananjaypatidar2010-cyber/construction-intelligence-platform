import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
PNG = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
       b"\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa7\x9a\xa0\xa0\x00\x00\x00\x00IEND\xaeB`\x82")


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"


def test_safety_and_crack():
    for path in ("/api/safety/analyze", "/api/cracks/analyze"):
        r = client.post(path, files={"image": ("a.png", io.BytesIO(PNG), "image/png")})
        assert r.status_code == 200, r.text


def test_rejects_non_image():
    r = client.post("/api/cracks/analyze", files={"image": ("a.txt", io.BytesIO(b"hi"), "text/plain")})
    assert r.status_code == 415


def test_valuation_and_planning():
    v = client.post("/api/valuation", json={"location": "Indore", "area_sqft": 1200})
    assert v.status_code == 200 and v.json()["estimated_value_low"] > 0
    p = client.post("/api/planning", json={"project_name": "Villa", "area_sqft": 2000, "budget": 5000000})
    assert p.status_code == 200 and p.json()["total_estimated_cost"] == 5000000


def test_validation_error():
    assert client.post("/api/valuation", json={"location": "x", "area_sqft": -5}).status_code == 422


def test_knowledge_and_daily():
    assert client.post("/api/knowledge/ask", json={"question": "How long to cure slabs?"}).status_code == 200
    assert client.post("/api/assistant/daily", json={"tasks_today": ["pour slab"]}).status_code == 200
