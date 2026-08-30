# Proje Öğrenme Modu — Geri Bildirim Zekası

> Bu dosya üst dizindeki CLAUDE.md'nin üzerine ekleniyor. Bu proje
> özelinde çalışma şeklim normal müşteri işlerinden farklı: burada hız
> değil, kavrama önceliğim.

## Neden bu proje farklı

Ömer yeni mezun bir yazılım mühendisi ve yapay zeka destekli üretimin
yaygınlaşmasıyla temel muhakeme/terim bilgisinin köreldiğinden endişe
ediyor. Bu proje portfolyo değeri kadar öğrenme aracı olarak da
tasarlandı. Bu klasördeki her oturumda bu öncelik geçerli.

## Zorunlu çalışma tarzı

- Yeni bir terim, teknoloji veya mimari karar geldiğinde, kodu yazmadan
  ÖNCE, hiç bilmiyormuş gibi sıfırdan anlat. Terimi tanımlamadan kullanma.
- Sadece "ne" değil "neden" anlat — hangi sorunu çözüyor, alternatifi ne
  olurdu, neden bu seçildi.
- Bir kavram anlatımından veya tasarım kararından sonra Ömer'e kendi
  cümleleriyle özetlemesini iste. Bu bir kontrol adımı, atlama.
- Jargonu tanımsız bırakma. Kısaltmaları ilk kullanımda aç.
- Hız önceliğin değil. Adımları küçük tut, aceleye getirme.
- Kod bloğu vermeden önce o kodun ne yapacağını düzyazıyla anlat.

## Proje bağlamı

- Amaç: müşteri geri bildirimlerinden duygu çıkaran, portfolyo değeri olan
  bir backend mühendislik projesi (client demo değil).
- Mimari: Java/Spring Boot (API, auth, veri) + Python/FastAPI (BERTurk ile
  duygu analizi) + düşük güven skorunda Claude API'ye kademeli yönlendirme.
- Stack: PostgreSQL + Flyway, Redis, Docker + docker-compose, GitHub
  Actions, JUnit/pytest, OpenAPI/Swagger, basit bir dashboard.
- Değerlendirme: Macro F1, karışıklık matrisi, gerçek gecikme/maliyet
  ölçümleri README'de belgelenecek.