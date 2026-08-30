import logging
from functools import lru_cache

from transformers import pipeline

from app.cache import onbellege_yaz, onbellekten_oku
from app.claude_client import ikinci_gorus_al

logger = logging.getLogger(__name__)

MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased"
GUVEN_ESIGI = 0.7


@lru_cache(maxsize=1)
def modeli_yukle():
    return pipeline("sentiment-analysis", model=MODEL_ADI)


def analiz_et(metin: str) -> tuple[str, float]:
    onbellek_sonucu = onbellekten_oku(metin)
    if onbellek_sonucu is not None:
        return onbellek_sonucu

    analizci = modeli_yukle()
    sonuc = analizci(metin)[0]
    duygu, guven = sonuc["label"].lower(), float(sonuc["score"])

    if guven < GUVEN_ESIGI:
        try:
            duygu, guven = ikinci_gorus_al(metin)
        except Exception as e:
            logger.warning("Claude'a ikinci görüş alınamadı: %s", e)

    onbellege_yaz(metin, duygu, guven)
    return duygu, guven
