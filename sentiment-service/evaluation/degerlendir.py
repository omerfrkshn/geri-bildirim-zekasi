"""
Duygu analizi hattının gerçek, etiketli bir veri seti üzerinde değerlendirilmesi.

Veri kaynağı: winvoker/turkish-sentiment-analysis-dataset (Hugging Face, CC-BY-SA 4.0)
https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset
"""

import csv
import random
import statistics
import time
from pathlib import Path
from unittest.mock import patch

import requests
from sklearn.metrics import confusion_matrix, f1_score

from app import sentiment
from app.cache import anahtar_uret, istemciyi_al

DEGERLENDIRME_DIZINI = Path(__file__).parent
HAM_VERI_DOSYASI = DEGERLENDIRME_DIZINI / "test_indirilen.csv"
ORNEK_DOSYASI = DEGERLENDIRME_DIZINI / "test_ornegi.csv"
SONUC_DOSYASI = DEGERLENDIRME_DIZINI / "sonuclar.md"

VERI_SETI_URL = (
    "https://huggingface.co/datasets/winvoker/"
    "turkish-sentiment-analysis-dataset/resolve/main/test.csv"
)

ORNEK_BOYUTU = 150
RASTGELE_TOHUM = 42
CLAUDE_CAGRI_BASINA_MALIYET_USD = 0.001

ETIKET_ESLEME = {
    "positive": "positive",
    "negative": "negative",
    "notr": "neutral",
    "neutral": "neutral",
}


def veri_setini_indir() -> None:
    if HAM_VERI_DOSYASI.exists():
        return
    print(f"Veri seti indiriliyor: {VERI_SETI_URL}")
    cevap = requests.get(VERI_SETI_URL, timeout=60)
    cevap.raise_for_status()
    HAM_VERI_DOSYASI.write_bytes(cevap.content)


def ornek_olustur() -> list[dict]:
    veri_setini_indir()
    with open(HAM_VERI_DOSYASI, encoding="utf-8") as dosya:
        satirlar = list(csv.DictReader(dosya))

    gecerli_satirlar = [
        s for s in satirlar if s.get("text", "").strip() and s.get("label", "").strip().lower() in ETIKET_ESLEME
    ]

    random.seed(RASTGELE_TOHUM)
    ornek = random.sample(gecerli_satirlar, ORNEK_BOYUTU)

    with open(ORNEK_DOSYASI, "w", encoding="utf-8", newline="") as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=["text", "label"])
        yazici.writeheader()
        for satir in ornek:
            yazici.writerow({"text": satir["text"], "label": satir["label"]})

    return [{"text": s["text"], "label": ETIKET_ESLEME[s["label"].strip().lower()]} for s in ornek]


def onbellegi_temizle(ornekler: list[dict]) -> None:
    istemci = istemciyi_al()
    anahtarlar = [anahtar_uret(o["text"]) for o in ornekler]
    if anahtarlar:
        istemci.delete(*anahtarlar)


def degerlendirmeyi_calistir(ornekler: list[dict]) -> dict:
    onbellegi_temizle(ornekler)

    gercek_etiketler = []
    tahmin_edilen_etiketler = []
    gecikmeler_saniye = []

    with patch.object(sentiment, "ikinci_gorus_al", wraps=sentiment.ikinci_gorus_al) as claude_izleyici:
        for i, ornek in enumerate(ornekler, start=1):
            baslangic = time.perf_counter()
            duygu, _guven = sentiment.analiz_et(ornek["text"])
            gecikmeler_saniye.append(time.perf_counter() - baslangic)

            gercek_etiketler.append(ornek["label"])
            tahmin_edilen_etiketler.append(duygu)

            if i % 25 == 0:
                print(f"  {i}/{len(ornekler)} tamamlandı")

        claude_cagri_sayisi = claude_izleyici.call_count

    return {
        "gercek": gercek_etiketler,
        "tahmin": tahmin_edilen_etiketler,
        "gecikmeler": gecikmeler_saniye,
        "claude_cagri_sayisi": claude_cagri_sayisi,
    }


def karisiklik_matrisi_markdown(gercek: list[str], tahmin: list[str], siniflar: list[str]) -> str:
    matris = confusion_matrix(gercek, tahmin, labels=siniflar)
    basliklar = " | ".join(siniflar)
    satirlar = [f"| Gerçek \\ Tahmin | {basliklar} |", "|---" * (len(siniflar) + 1) + "|"]
    for sinif_adi, satir in zip(siniflar, matris):
        degerler = " | ".join(str(deger) for deger in satir)
        satirlar.append(f"| **{sinif_adi}** | {degerler} |")
    return "\n".join(satirlar)


def rapor_uret(sonuc: dict) -> str:
    siniflar = ["positive", "negative", "neutral"]
    macro_f1 = f1_score(sonuc["gercek"], sonuc["tahmin"], labels=siniflar, average="macro")
    gecikmeler = sonuc["gecikmeler"]
    tahmini_maliyet = sonuc["claude_cagri_sayisi"] * CLAUDE_CAGRI_BASINA_MALIYET_USD

    return f"""# Değerlendirme Sonuçları

Veri kaynağı: [winvoker/turkish-sentiment-analysis-dataset](https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset) (CC-BY-SA 4.0), test bölümünden rastgele {ORNEK_BOYUTU} örnek (`random_state={RASTGELE_TOHUM}`, bkz. `test_ornegi.csv`).

## Doğruluk

- **Macro F1:** {macro_f1:.3f}

### Karışıklık Matrisi

{karisiklik_matrisi_markdown(sonuc["gercek"], sonuc["tahmin"], siniflar)}

## Gecikme (Latency)

- Ortalama: {statistics.mean(gecikmeler):.3f} sn
- Medyan: {statistics.median(gecikmeler):.3f} sn
- En yavaş (p95): {statistics.quantiles(gecikmeler, n=20)[18]:.3f} sn

## Maliyet

- Claude'a yönlendirilen örnek sayısı: {sonuc["claude_cagri_sayisi"]} / {ORNEK_BOYUTU}
- Tahmini maliyet: ${tahmini_maliyet:.4f} (örnek başına ~${CLAUDE_CAGRI_BASINA_MALIYET_USD} varsayımıyla)
"""


def main() -> None:
    print("Örnek hazırlanıyor...")
    ornekler = ornek_olustur()
    print(f"{len(ornekler)} örnek üzerinde değerlendirme başlıyor...")
    sonuc = degerlendirmeyi_calistir(ornekler)
    rapor = rapor_uret(sonuc)
    SONUC_DOSYASI.write_text(rapor, encoding="utf-8")
    print(rapor)
    print(f"\nRapor kaydedildi: {SONUC_DOSYASI}")


if __name__ == "__main__":
    main()
