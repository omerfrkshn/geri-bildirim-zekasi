import json
import os
from functools import lru_cache

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL_ADI = "claude-haiku-4-5"

SISTEM_TALIMATI = (
    "Sen bir müşteri geri bildirimi duygu analizi asistanısın. "
    "Sana verilen Türkçe metni positive, negative veya neutral olarak sınıflandır. "
    'Cevabını SADECE şu JSON formatında ver, başka hiçbir açıklama ekleme: '
    '{"duygu": "positive|negative|neutral", "guven": 0.0-1.0}'
)


@lru_cache(maxsize=1)
def istemciyi_al() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def ikinci_gorus_al(metin: str) -> tuple[str, float]:
    istemci = istemciyi_al()
    cevap = istemci.messages.create(
        model=MODEL_ADI,
        max_tokens=100,
        system=SISTEM_TALIMATI,
        messages=[{"role": "user", "content": metin}],
    )
    metin_cevap = cevap.content[0].text.strip()
    metin_cevap = metin_cevap.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    veri = json.loads(metin_cevap)
    return veri["duygu"], float(veri["guven"])
