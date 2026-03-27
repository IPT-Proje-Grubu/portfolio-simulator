# Portfolio Simulator

Gelişmiş bir Python tabanlı portföy yönetimi, kripto/hisse analiz ve interaktif öğrenme uygulaması.  
PyQt6 ile yazılmış, masaüstü (Windows/macOS/Linux) ortamında çalışan, Google Gemini AI destekli bir eğitim ve simülasyon platformudur.

---

## Kişisel Bilgisayarda Çalıştırma

```powershell
# 1. Proje klasörüne git
cd C:\Users\kerem\portfolio-simulator
# 2. Sanal ortam oluştur  (ilk seferde bir kez yapılır)
python -m venv venv
# 3. Sanal ortamı etkinleştir
.\venv\Scripts\Activate.ps1
# 4. Gerekli paketleri yükle  (ilk seferde bir kez yapılır)
pip install PyQt6

#*ŞİMDİLİK BUNU YAPMAYIN!
pip install google-generativeai   # AI Koç özelliği için (isteğe bağlı) 
# 5. Uygulamayı başlat
python main.py
```
> **Not:** Sonraki açılışlarda sadece 1. 3. ve 5. adımları çalıştırman yeterli.
---

## Özellikler

### Portföy Yönetimi
- Gerçek zamanlı simüle fiyatlarla alım/satım emirleri (3 saniyede bir güncellenir)
- Açık pozisyon takibi: ortalama maliyet, piyasa değeri, gerçekleşmemiş/gerçekleşmiş K/Z
- Portföy değer geçmişi ve grafik görselleştirme
- Nakit bakiye yönetimi ve işlem geçmişi

### Analiz Modülü
- Seçili tarih aralığında senaryo simülasyonu
- Doğrusal regresyon tabanlı tahmin (RegressionForecaster)
- Trend yönü, değişim yüzdesi ve volatilite hesaplama
- 6 adımlık tahmin noktaları tablosu

### Veri İşleme
- CSV dosyası yükleme ve otomatik kolon haritası analizi
- Tarih/fiyat kolonu otomatik tespiti
- Temizlenmiş veri seti yönetimi

### Öğrenme Modu (15 Görev, 3 Seviye)
Kullanıcı sıralı görevleri tamamlayarak XP kazanır ve seviyeleri açar.

| Seviye | Gerekli XP | Görev Sayısı | Konu |
|--------|-----------|--------------|------|
| 🌱 Başlangıç | 0 XP | 5 görev | İlk alım, satış, portföy inceleme, analiz, rapor |
| 📈 Orta | 300 XP | 5 görev | Çeşitlendirme, kârlı satış, büyük alım, tahmin, hesap makinesi |
| 🚀 İleri | 700 XP | 5 görev | Dengeli portföy, büyük kârlı satış, tam döngü, çoklu satış, büyük tahmin |

- **Seviye kilitleme:** Bir seviyeyi tamamlamadan bir sonraki açılmaz
- **Gamification:** XP sistemi, rozet ödülleri, liderboard
- **Başarımlar ve Meydan Okumalar:** Özel koşullarla tetiklenen ek ödüller

### "Hatadan Öğren" Sistemi
Her alım/satım sonrası kural tabanlı hata tespiti:

| Kural | Tetikleyici | Önerilen Aksiyon |
|-------|------------|------------------|
| Aşırı konsantrasyon | Tek varlık > %55 portföy | Çeşitlendirme yap |
| Büyük tek işlem | İşlem > nakit'in %50'si | Daha küçük alımlar yap |
| Zararda panik satış | Kayıp > -%20 | Uzun vadeli düşün |
| Kazanan erken sat | Kâr < %5 iken sat | Pozisyonu tut |
| Çeşitlilik yok | Sadece 1 varlık | Farklı sektörler ekle |
| Atıl nakit | Nakit > %80 portföy | Yatırım değerlendirmesi yap |
| Aşırı işlem | 10+ işlem, kazan oranı < %30 | İşlem sıklığını azalt |

### AI Koç Sistemi (Gemini + Kural Tabanlı Hibrit)
- **Kural tabanlı analiz:** API bağlantısı olmadan da çalışır, anlık portföy durumuna göre öneri üretir
- **Gemini AI:** Gerçek portföy verisiyle zenginleştirilmiş bağlamsal öneriler
- **Soru-Cevap:** Kullanıcı soru sorar, AI gerçek portföy verisine bakarak yanıtlar
- **Görev ipucu:** Öğrenme modundayken cevabı vermeden yönlendirici ipuçları
- **Asenkron çalışma:** API çağrıları arka planda çalışır, arayüz donmaz

### Liderboard Sistemi
- Oturum başına rastgele Türkçe kullanıcı adı atanır (giriş gerektirmez)
- `leaderboard.json` dosyasına yerel olarak kaydedilir
- Toplam K/Z, işlem sayısı, kazanma oranı, risk skoru ve seviyeye göre sıralama
- İlk 10 oyuncu görüntülenir

---

## Proje Yapısı

```
portfolio-simulator/
│
├── main.py                         # Uygulama giriş noktası
├── requirements.txt                # Bağımlılıklar
├── .env.example                    # API anahtarı örnek dosyası
├── leaderboard.json                # Liderboard verileri (otomatik oluşturulur)
│
└── src/
    ├── app.py                      # PyQt6 uygulama bootstrap
    │
    ├── ai/                         # AI Koç modülleri
    │   ├── gemini_service.py       # Gemini API katmanı (önbellekleme, async)
    │   ├── context_builder.py      # Portföy durumundan AI bağlamı oluşturma
    │   └── ai_coach.py             # Hibrit AI sistemi + kural motoru
    │
    ├── learning/                   # Öğrenme sistemi
    │   ├── manager.py              # LearningManager, LearningExtra, Achievement, Challenge
    │   ├── level.py                # Level sınıfı
    │   ├── task.py                 # Task sınıfı ve TaskStatus
    │   ├── mistake_detector.py     # Hata tespiti ve uyarı sistemi
    │   ├── leaderboard.py          # LeaderboardManager, JSON kalıcılığı
    │   └── system.py               # Geriye dönük uyumluluk alias'ları
    │
    ├── portfolio/                  # Portföy iş mantığı
    │   ├── portfolio.py            # PortfolioState, işlem motoru
    │   ├── asset.py                # Position veri modeli
    │   ├── trade.py                # Trade veri modeli
    │   └── market.py               # PriceFeed, WATCHLIST, fiyat simülasyonu
    │
    ├── analysis/                   # Analiz motoru
    │   ├── regression_model.py     # RegressionForecaster
    │   └── trend_analysis.py       # TrendAnalyzer, TrendSummary
    │
    ├── data_processing/            # CSV işleme
    │   ├── data_loader.py          # DataLoader, DatasetInfo
    │   └── data_cleaner.py         # DataCleaner, CleanedDataset
    │
    ├── alerts/                     # Uyarı sistemi
    │   └── alert_system.py         # AlertSystem
    │
    ├── education/                  # Eğitim içerikleri
    │   ├── content.py              # GLOSSARY, TIPS, TOPICS, TUTORIAL_STEPS
    │   └── widgets.py              # Eğitim widget'ları
    │
    ├── ui/                         # Kullanıcı arayüzü
    │   ├── main_window.py          # Ana pencere ve tüm sayfalar
    │   ├── learn_page.py           # Öğrenme modu sayfası (LevelPage, AICoachPage…)
    │   └── welcome_dialog.py       # Karşılama ekranı
    │
    └── visualization/              # Grafik bileşenleri
        ├── charts.py               # ChartPlaceholder (çizgi/pasta grafik)
        └── portfolio_chart.py      # Portföy dilim hesaplama
```

---

## Sayfalar

| # | Sayfa | Açıklama |
|---|-------|----------|
| 0 | **Dashboard** | Portföy özeti, XP ilerleme, aktif görev, AI önerisi, risk rozeti |
| 1 | **İşlem** | Alım/satım emri, açık pozisyonlar, hesap özeti, görev banner'ı |
| 2 | **Geçmiş** | İşlem geçmişi tablosu, kazanma oranı, kârlı satımlar, risk skoru |
| 3 | **Veri** | CSV yükleme ve kolon haritası analizi |
| 4 | **Analiz** | Senaryo simülasyonu, trend analizi, AI Koç yorumu |
| 5 | **Öğren** | Görevler, başarımlar, meydan okumalar, liderboard, AI Koç |

---

## AI Koç Kurulumu (İsteğe Bağlı)

AI Koç sistemi API anahtarı olmadan **kural tabanlı modda** tam çalışır.  
Gemini ile güçlendirmek için:

**1. Ücretsiz API anahtarı al:**  
[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**2. `.env` dosyası oluştur:**
```powershell
Copy-Item .env.example .env
```

**3. Dosyayı düzenle:**
```
GEMINI_API_KEY=buraya_api_anahtarını_yapıştır
```

**4. Alternatif:** Uygulamayı açtıktan sonra **Öğren → AI Koç** sekmesinden API anahtarını doğrudan girebilirsin.

---

## Gereksinimler

| Paket | Versiyon | Zorunlu | Açıklama |
|-------|---------|---------|----------|
| Python | >= 3.10 | Evet | f-string, match, type hint desteği için |
| PyQt6 | >= 6.10.2 | Evet | Masaüstü GUI framework |
| google-generativeai | >= 0.8.6 | Hayır | Gemini AI desteği |

```powershell
pip install -r requirements.txt
```

---

## XP ve Seviye Sistemi

```
0 XP ──────── 300 XP ──────── 700 XP ──────── 1200 XP
  🌱 Başlangıç   📈 Orta          🚀 İleri         🏆 Usta
  (5 görev)      (5 görev)        (5 görev)
```

- Her görev tamamlandığında **100–200 XP** kazanılır
- Başarımlar ekstra **50–150 XP** sağlar
- Meydan okumalar ekstra **100–200 XP** sağlar
- Bir seviyeyi tamamlamadan bir sonraki kilidini açamazsın

---

## Mimari Tasarım Kararları

**OOP Prensipler:**
- `Task`, `Level`, `LearningManager` tamamen birbirinden bağımsız sınıflar
- `PortfolioState` iş mantığını taşır; UI ona bağımlı, o UI'a bağımlı değil
- `AICoach`, `GeminiService`'i bir bağımlılık olarak alır — kolay swap/mock
- `MistakeDetector` saf fonksiyonlar üzerine kurulu, state tutmaz

**Asenkron AI çağrıları:**
- `GeminiWorker(QThread)` API çağrılarını arka planda çalıştırır
- Ana thread hiçbir zaman bloklanmaz
- Callback mekanizması ile sonuçlar UI'a iletilir

**Kalıcılık:**
- `leaderboard.json` — liderboard verileri
- `.env` — API anahtarları (git'e eklenmez)
- Portföy state'i şu an bellekte tutulur (oturum başına sıfırlanır)

---

## Ekran Görüntüleri

> Uygulama tamamen koyu tema (dark mode) üzerine tasarlanmıştır.  
> Renk paleti: `#0b0f1a` arka plan, `#2563eb` vurgu, `#10b981` yeşil, `#ef4444` kırmızı.

---

## Geliştirici Notları

- Tüm Python dosyaları `from __future__ import annotations` ile başlar (Python 3.9 uyumluluğu için)
- Sabitler `_BIG_CAPS` şeklinde özel adlandırılmış
- UI bileşenleri `_lbl()`, `_btn()`, `_card()`, `_metric()` yardımcıları ile standartlaştırılmış
- Linting: PyLance / Pylint ile hatasız
- Test dosyaları: `tests/test_portfolio.py`, `tests/test_alerts.py`
