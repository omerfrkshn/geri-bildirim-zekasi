from fastapi.testclient import TestClient

from app import main, sentiment


def test_analiz_et_endpoint_modeli_cagirip_sonucu_dondurur(monkeypatch):
    monkeypatch.setattr(main, "analiz_et", lambda metin: ("positive", 0.91))
    client = TestClient(main.app)

    response = client.post("/analiz-et", json={"metin": "harika hizmet"})

    assert response.status_code == 200
    assert response.json() == {"duygu": "positive", "guven": 0.91}


def test_analiz_et_dusuk_guvende_claudeye_yonlenir(monkeypatch):
    monkeypatch.setattr(
        sentiment, "modeli_yukle", lambda: (lambda metin: [{"label": "NEUTRAL", "score": 0.4}])
    )
    monkeypatch.setattr(sentiment, "ikinci_gorus_al", lambda metin: ("negative", 0.88))

    duygu, guven = sentiment.analiz_et("idare eder, pek bir sey diyemeyecegim")

    assert duygu == "negative"
    assert guven == 0.88


def test_analiz_et_yuksek_guvende_claudeye_yonlenmez(monkeypatch):
    monkeypatch.setattr(
        sentiment, "modeli_yukle", lambda: (lambda metin: [{"label": "POSITIVE", "score": 0.95}])
    )

    def claude_cagrilmamali(metin):
        raise AssertionError("Claude çağrılmamalı")

    monkeypatch.setattr(sentiment, "ikinci_gorus_al", claude_cagrilmamali)

    duygu, guven = sentiment.analiz_et("harika bir deneyimdi")

    assert duygu == "positive"
    assert guven == 0.95


def test_analiz_et_claude_basarisiz_olursa_orijinal_sonuca_doner(monkeypatch):
    monkeypatch.setattr(
        sentiment, "modeli_yukle", lambda: (lambda metin: [{"label": "NEUTRAL", "score": 0.4}])
    )

    def claude_patlar(metin):
        raise RuntimeError("bağlantı hatası")

    monkeypatch.setattr(sentiment, "ikinci_gorus_al", claude_patlar)

    duygu, guven = sentiment.analiz_et("idare eder")

    assert duygu == "neutral"
    assert guven == 0.4
