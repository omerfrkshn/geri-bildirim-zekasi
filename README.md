# Geri Bildirim Zekası

Müşteri geri bildirimlerinden duygu (sentiment) çıkaran bir backend mühendislik projesi.

## Mimari

- **api-service** (Java / Spring Boot): API, kimlik doğrulama, veri yönetimi.
- **sentiment-service** (Python / FastAPI): BERTurk ile duygu analizi; düşük güven skorunda Claude API'ye kademeli yönlendirme.
- **PostgreSQL + Flyway**: veri ve şema yönetimi.
- **Redis**: önbellekleme.
- **Docker Compose**: yerel geliştirme ortamı.
- **GitHub Actions**: CI (test otomasyonu).

- **dashboard**: Statik HTML/CSS/JS (Chart.js, CDN), CORS ile API'ye bağlanan görsel arayüz.

## Durum

Faz 0-7 tamamlandı: uçtan uca mimari, dashboard ve değerlendirme çalışıyor. Sonraki adım: ironi/alaycılık katmanı (Versiyon 2, ayrı bir faz olarak planlandı).

## Değerlendirme

Değerlendirme metodolojisi ve script'i: [`sentiment-service/evaluation/degerlendir.py`](sentiment-service/evaluation/degerlendir.py).
Ham sonuçlar: [`sentiment-service/evaluation/sonuclar.md`](sentiment-service/evaluation/sonuclar.md).

Veri kaynağı: [winvoker/turkish-sentiment-analysis-dataset](https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset) (Hugging Face, CC-BY-SA 4.0) — test bölümünden rastgele seçilmiş 150 örnek (`random_state=42`, tekrarlanabilir; örnek kendisi `sentiment-service/evaluation/test_ornegi.csv`'de).

- **Macro F1:** 0.444
- **Karışıklık matrisi:** modelin en belirgin zayıflığı, pozitif metinleri sıkça (93 örnekten 30'u) negatif olarak sınıflandırması — sonuçların detayı `sonuclar.md`'de.
- **Gecikme:** ortalama 0.188 sn, p95 1.021 sn (Claude'a yönlendirilen örnekler p95'i yukarı çekiyor)
- **Maliyet:** 150 örnekten 18'i (%12) Claude'a yönlendirildi, tahmini maliyet $0.018

**Bilinen sınırlama:** BERTurk tabanlı model, ironi/alaycılık ve pozitif kelimelerle örtülü olumsuz yorumlarda zayıf — bu, Versiyon 2'de ayrı bir katmanla ele alınması planlanan bir konu.
