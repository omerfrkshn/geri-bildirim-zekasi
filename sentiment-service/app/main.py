from fastapi import FastAPI

from app.schemas import AnalizCevap, AnalizIstek
from app.sentiment import analiz_et

app = FastAPI(title="Duygu Analizi Servisi")


@app.post("/analiz-et", response_model=AnalizCevap)
def analiz_et_endpoint(istek: AnalizIstek) -> AnalizCevap:
    duygu, guven = analiz_et(istek.metin)
    return AnalizCevap(duygu=duygu, guven=guven)
