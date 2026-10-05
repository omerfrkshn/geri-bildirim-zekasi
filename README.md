# Geri Bildirim Zekası

![CI](https://github.com/omerfrkshn/geri-bildirim-zekasi/actions/workflows/ci.yml/badge.svg)

Müşteri geri bildirimlerinden duygu çıkaran, iki servisli küçük bir backend projesi. Amaç bir ürün değil. Mikroservis mimarisi, servisler arası REST iletişimi, bir LLM'e kademeli yönlendirme ve gerçek veriyle model değerlendirmesi gibi konuları uçtan uca, çalışan bir sistem üzerinde göstermek.

## Nasıl çalışıyor

Bir geri bildirim geldiğinde `api-service` (Java/Spring Boot) onu veritabanına kaydeder ve duygusunu öğrenmek için `sentiment-service`'e (Python/FastAPI) bir istek atar. Orada Hugging Face'ten aldığım, Türkçe duygu analizi için eğitilmiş hazır bir BERT modeli (`savasy/bert-base-turkish-sentiment-cased`) metni sınıflandırır. Modeli ben eğitmedim, hazır haliyle kullanıyorum. Modelin güven skoru düşükse (`<0.7`), sonuç Redis'e yazılmadan önce Claude Haiku'ya ikinci bir görüş için gönderilir. Böylece modelin emin olamadığı örnekler daha güçlü bir modelle çözülür, ama her istek için pahalı bir LLM çağrısı yapılmaz.

Python servisi hiçbir aşamada erişilemez olursa (kapalı, timeout, vs.) geri bildirim yine de kaydedilir, sadece duygu alanı boş kalır. Bir alt servisin çökmesi ana işlevi durdurmaz.

```
Kullanıcı → api-service (Java) → sentiment-service (Python)
                                       ├─ BERTurk (hızlı, ücretsiz)
                                       ├─ güven düşükse → Claude Haiku
                                       └─ Redis cache (7 gün TTL)
```

## Servisler

| Servis | Ne yapar |
|---|---|
| `api-service` | Spring Boot API. Geri bildirimleri kaydeder, listeler, sentiment-service'i çağırır |
| `sentiment-service` | FastAPI. BERTurk ile duygu analizi, düşük güvende Claude'a yönlendirme, Redis cache |
| `dashboard` | Statik HTML/JS + Chart.js. Duygu dağılımını ve geri bildirim akışını gösterir |
| PostgreSQL + Flyway | veri ve şema yönetimi |
| Redis | duygu analizi sonuçlarının önbelleği |

## Kurulum ve çalıştırma

Gerekenler: Docker, Java 21, Maven, Python 3.12 (3.13 ve üstü değil, ML kütüphaneleri henüz desteklemiyor).

```bash
# 1. Veritabanı ve cache
docker compose up -d

# 2. Python servisi (ayrı bir terminalde)
cd sentiment-service
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt   # Linux/Mac: .venv/bin/pip
cp .env.example .env   # ANTHROPIC_API_KEY'ini içine yaz
.venv\Scripts\python -m uvicorn app.main:app --port 8000

# 3. Java servisi (ayrı bir terminalde)
cd api-service
mvn spring-boot:run

# 4. Dashboard (ayrı bir terminalde)
cd dashboard
python -m http.server 8081
```

Dashboard `http://localhost:8081`'de açılır. Yeni bir geri bildirim eklemek için:

```bash
curl -X POST http://localhost:8080/geribildirimler \
  -H "Content-Type: application/json" \
  -d '{"metin":"kargo cok hizli geldi, tesekkurler"}'
```

## Testler

```bash
cd api-service && mvn test
cd sentiment-service && python -m pytest tests/
```

İkisi de tamamen mock'lu. Gerçek veritabanı, Redis ya da Claude API'sine ihtiyaç duymuyor. `.github/workflows/ci.yml` her push'ta ikisini de otomatik çalıştırıyor.

## Değerlendirme

Modelin gerçekten ne kadar iyi çalıştığını görmek için sentetik değil, gerçek bir Türkçe veri seti kullandım: [winvoker/turkish-sentiment-analysis-dataset](https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset) (CC-BY-SA 4.0). Test bölümünden rastgele 150 örnek seçip (`random_state=42`, tekrarlanabilir, bkz. `sentiment-service/evaluation/`) tüm hattan geçirdim.

- **Macro F1: 0.444.** İdeal değil, ve neden olduğu da açık: karışıklık matrisine bakınca model pozitif metinlerin neredeyse üçte birini (93'ün 30'u) negatif olarak etiketliyor. En büyük zayıflık burada. İkinci etken sınıf dengesi: örneklemin 46'sı (%31) nötr, ama bunların yalnızca 8'i nötr olarak bulundu (25'i pozitif, 13'ü negatif sanıldı). Nötr tahminlerin tamamı (8) doğru çıktı, yani sorun yanlış nötr demek değil, nötrü yakalayamamak.
- **Gecikme:** ortalama 0.188 sn, p95 1.021 sn. Aradaki fark büyük ölçüde Claude'a giden örneklerden kaynaklanıyor.
- **Maliyet:** 150 örnekten 18'i (%12) Claude'a yönlendirildi, tahmini maliyet $0.018.

Tam rapor ve script: [`sentiment-service/evaluation/`](sentiment-service/evaluation/).

## Bilinen sınırlama ve sonraki adım

BERTurk tabanlı model ironi, alaycılık ve pozitif kelimelerle örtülü olumsuz yorumlarda zayıf. Türkçe'de bu tür ifadeler oldukça yaygın olduğu için gerçek bir eksik. Bunu bir sonraki sürümde (V2) ayrı bir katman olarak ele almayı planlıyorum: şüpheli metinleri, BERTurk'ün güven skorundan bağımsız olarak Claude'a yönlendiren ek bir kontrol.

## Lisans

MIT, bkz. [LICENSE](LICENSE).
