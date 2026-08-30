from fastapi.testclient import TestClient

from app import main


def test_analiz_et_endpoint_modeli_cagirip_sonucu_dondurur(monkeypatch):
    monkeypatch.setattr(main, "analiz_et", lambda metin: ("positive", 0.91))
    client = TestClient(main.app)

    response = client.post("/analiz-et", json={"metin": "harika hizmet"})

    assert response.status_code == 200
    assert response.json() == {"duygu": "positive", "guven": 0.91}
