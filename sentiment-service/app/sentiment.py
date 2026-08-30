from functools import lru_cache

from transformers import pipeline

MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased"


@lru_cache(maxsize=1)
def modeli_yukle():
    return pipeline("sentiment-analysis", model=MODEL_ADI)


def analiz_et(metin: str) -> tuple[str, float]:
    analizci = modeli_yukle()
    sonuc = analizci(metin)[0]
    return sonuc["label"].lower(), float(sonuc["score"])
