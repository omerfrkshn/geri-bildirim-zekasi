# Değerlendirme Sonuçları

Veri kaynağı: [winvoker/turkish-sentiment-analysis-dataset](https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset) (CC-BY-SA 4.0), test bölümünden rastgele 150 örnek (`random_state=42`, bkz. `test_ornegi.csv`).

## Doğruluk

- **Macro F1:** 0.444

### Karışıklık Matrisi

| Gerçek \ Tahmin | positive | negative | neutral |
|---|---|---|---|
| **positive** | 63 | 30 | 0 |
| **negative** | 0 | 11 | 0 |
| **neutral** | 25 | 13 | 8 |

## Gecikme (Latency)

- Ortalama: 0.188 sn
- Medyan: 0.050 sn
- En yavaş (p95): 1.021 sn

## Maliyet

- Claude'a yönlendirilen örnek sayısı: 18 / 150
- Tahmini maliyet: $0.0180 (örnek başına ~$0.001 varsayımıyla)
