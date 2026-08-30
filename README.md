# Geri Bildirim Zekası

Müşteri geri bildirimlerinden duygu (sentiment) çıkaran bir backend mühendislik projesi.

## Mimari

- **api-service** (Java / Spring Boot): API, kimlik doğrulama, veri yönetimi.
- **sentiment-service** (Python / FastAPI): BERTurk ile duygu analizi; düşük güven skorunda Claude API'ye kademeli yönlendirme.
- **PostgreSQL + Flyway**: veri ve şema yönetimi.
- **Redis**: önbellekleme.
- **Docker Compose**: yerel geliştirme ortamı.
- **GitHub Actions**: CI (test otomasyonu).

## Durum

Faz 0 — iskelet kuruldu. Sonraki adım: `api-service` içinde Spring Boot projesinin temel CRUD API'si.

## Değerlendirme (ilerledikçe doldurulacak)

- Macro F1
- Karışıklık matrisi (confusion matrix)
- Gerçek gecikme ve maliyet ölçümleri
