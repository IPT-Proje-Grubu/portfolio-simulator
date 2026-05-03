# PortfolioSim — Sayfa Rehberi

Uygulamadaki tüm sayfaların ve bölümlerin açıklaması.

---

## Ana Navigasyon

Sol kenar çubuğunda 5 ana sayfa yer alır.

---

### ◎ Özet (Dashboard)

Portföyün genel durumunu tek bakışta gösteren ana ekrandır.

**Ne içerir:**
- **5 metrik kutusu:** Portföy değeri, Toplam K/Z, Gerçekleşmemiş K/Z, Gerçekleşmiş K/Z, Öğrenme seviyesi/XP
- **Portföy Değer Grafiği:** Zaman içindeki değer değişimini gösteren çizgi grafik
- **Piyasa (Canlı):** Tüm varlıkların anlık fiyatı ve yüzdelik değişimi — her 3 saniyede güncellenir
- **Son İşlemler:** En son alım/satım işlemlerinin özeti
- **Öğrenme Paneli:** Aktif görev ve XP ilerleme çubuğu
- **AI Koç Önerisi:** Portföy durumuna göre Gemini tarafından üretilen anlık öneri
- **Hızlı Erişim Butonları:** İşlem ve Analiz sayfalarına kısayol

---

### ⇄ İşlem (Trade)

Varlık alım ve satımının gerçekleştirildiği sayfadır.

**Ne içerir:**
- **Piyasa Listesi:** Tüm varlıklar (kripto, hisse, emtia), anlık fiyat ve değişim yüzdesiyle birlikte listelenir; bir satıra tıklanarak seçilir
- **Varlık Bilgisi:** Seçilen varlığın adı, sembolü, risk seviyesi ve açıklaması
- **Eğitim İçeriği:** Seçilen varlık hakkında risk kategorisi ve kısa açıklama
- **İşlem Formu:**
  - ALIM / SATIM modu seçimi
  - Miktar girişi (adet veya TL bazında)
  - "Maksimum" butonu ile tüm nakit/pozisyonu kullanma
  - İşlem özeti (toplam tutar, birim fiyat)
  - İşlemi gerçekleştir butonu
- **Pozisyonlar Tablosu:** Elinizdeki tüm açık pozisyonlar; sembol, adet, ortalama maliyet, anlık değer, K/Z ve "Kapat" butonu
- **Uyarılar:** Risk yönetimi uyarıları (yüksek konsantrasyon, zarar eşiği vb.)

---

### ≡ Geçmiş (History)

Gerçekleştirilen tüm alım/satım işlemlerinin kaydını gösterir.

**Ne içerir:**
- **İşlem Tablosu:** Tarih, işlem tipi (ALIM/SATIM), sembol, adet, fiyat, toplam tutar sütunlarıyla tüm geçmiş işlemler
- **Özet İstatistikler:** Toplam işlem sayısı, toplam alım, toplam satım, en iyi ve en kötü işlem
- **Filtreleme:** İşlem geçmişini sembol veya tarihe göre filtreleme imkânı

---

### ⊙ Analiz (Analysis)

Portföyün geçmiş ve gelecek performansını analiz etmek için senaryo simülasyonu yapılan sayfadır.

**Ne içerir:**
- **Senaryo Simülasyonu:**
  - Başlangıç ve bitiş tarihi seçimi (CSV verilerine dayalı)
  - "▶ Senaryo Simülasyonu Çalıştır" butonu
  - Gerçek tarihsel fiyatlarla portföyün o dönemdeki değerini hesaplar
- **Tahmin (Forecast) Tablosu:** Regresyon modeli kullanılarak 30 güne kadar fiyat tahmini
- **Trend Analizi:** Her varlık için yükseliş/düşüş trendi, volatilite ve momentum göstergeleri
- **Grafik:** Senaryo sonrası portföy değer grafiği
- **Senaryo Özeti:** Toplam K/Z, en iyi/en kötü performans gösteren varlık

---

### 📚 Öğren (Learn)

Yatırım kavramlarını görevler, başarımlar ve AI koçluk ile öğretmek için tasarlanmış etkileşimli öğrenme modudur.

Kendi içinde 9 alt bölüme sahiptir:

---

#### 🌱 Başlangıç

Yeni başlayanlar için temel görevler içerir.

**Örnek görevler:** İlk varlık alımı, portföy özetini görüntüleme, ilk satış, işlem geçmişini inceleme.

Her görev; açıklama, ipucu butonu, ilgili sayfaya yönlendirme ve otomatik doğrulama içerir. Görev tamamlandığında XP kazanılır.

---

#### 📈 Orta

Başlangıç seviyesi tamamlandıktan sonra açılır. Daha kapsamlı yatırım davranışlarını içerir.

**Örnek görevler:** Portföyü çeşitlendirme, risk oranını belirli seviyenin altına indirme, kârlı işlem kapama.

---

#### 🚀 İleri

Orta seviye tamamlandıktan sonra açılır. Analiz ve araç kullanımını kapsar.

**Örnek görevler:** Senaryo analizi çalıştırma, tahmin grafiğini inceleme, hesaplayıcı araçları kullanma.

---

#### 🏆 Başarımlar

Belirli koşulları sağlayınca otomatik olarak kazanılan rozetler.

**Örnekler:** İlk alım, ilk kârlı satış, belirli XP seviyesine ulaşma, portföyü çeşitlendirme. Her başarım ekstra XP verir.

---

#### ⚡ Zorluklar

Gerçek yatırım kararları almayı gerektiren özel görevlerdir. Tamamlanması daha fazla XP kazandırır.

**Örnekler:** Belirli bir kâr hedefine ulaşma, risk seviyesini düşürme, çok sayıda işlem gerçekleştirme.

---

#### 📊 Analizlerim

Kullanıcının öğrenme sürecindeki işlem performansını analiz eder.

**Ne içerir:**
- Toplam işlem sayısı, alım/satım sayısı, toplam hacim
- Toplam K/Z, gerçekleşmiş K/Z, gerçekleşmemiş K/Z
- Risk seviyesi
- En iyi ve en kötü satış işlemi

---

#### 🏅 Liderlik (Leaderboard)

Oturum bazlı liderlik tablosudur. Skorlar `leaderboard.json` dosyasına kaydedilir.

**Ne içerir:**
- Kendi sıranız, kullanıcı adınız, K/Z, işlem sayısı ve XP bilgileri
- En iyi 10 kullanıcının tablosu (K/Z'a göre sıralı)
- "Skoru Kaydet" butonu ile mevcut oturumu kaydetme

---

#### 🧮 Araçlar

İnteraktif finansal hesaplama araçları içerir.

**K/Z Hesaplayıcı:**
Alış fiyatı, mevcut fiyat ve adet girerek kar/zarar tutarını ve yüzdesini hesaplar.

**DCA Simülatörü (Dollar Cost Averaging):**
Aylık düzenli yatırımın belirli bir süre sonundaki toplam değerini hesaplar. Düzenli küçük miktarların bileşik etkisini gösterir.

> Bu araçlara dokunmak, "İleri" seviyesindeki **Hesaplayıcıları Kullan** görevini otomatik tamamlar.

---

#### 🤖 AI Koç

Gemini AI ile desteklenen kişisel finans koçluk sayfasıdır. Tüm öneriler gerçek portföy verilerine dayanır.

**Ne içerir:**
- **Gemini bağlantı durumu** (yeşil = bağlı, sarı = bağlantı yok)
- **Akıllı Öneri Şeridi:** Her işlem sonrası portföy durumuna göre otomatik üretilen öneri; "↻ Yenile" butonu ile güncellenebilir
- **Soru Sor (Ana Bölüm):** Büyük metin kutusu ile portföyünüz hakkında serbest soru sorulabilir
  - Hızlı soru chip'leri: *Portföy riskimi nasıl düşürürüm?*, *En iyi işlemim hangisi?*, *Şu an ne almalıyım?*, *Neden zarar ediyorum?*
- **AI Yanıtı:** Soruya Gemini tarafından verilen Türkçe, veriye dayalı yanıt
- **Görev İpucu:** Aktif öğrenme görevi için AI destekli ipucu
- **Portföy Anlık Durum:** Toplam değer, nakit, K/Z, risk seviyesi özeti

---

## Diyaloglar (Açılış Ekranları)

### Hoş Geldiniz Diyaloğu

Uygulama ilk açıldığında gösterilir. Kullanıcıya iki seçenek sunar:
- **Öğrenme Moduyla Başla** → Doğrudan Öğren sayfasına yönlendirir
- **Keşfet** → Ana sayfadan serbest kullanıma başlar

### Giriş / Kayıt Diyaloğu

Kullanıcı adı ve şifre ile giriş veya yeni hesap oluşturma ekranıdır. Veriler yerel SQLite veritabanına (`data/portfoliosim.db`) kaydedilir. Her kullanıcının portföyü ve işlem geçmişi ayrı tutulur.

---

## Teknik Notlar

| Bileşen | Açıklama |
|---------|----------|
| `data/raw/*.csv` | Kripto ve hisse senedi tarihsel fiyat verileri |
| `data/portfoliosim.db` | Kullanıcı hesapları, portföy ve işlem geçmişi |
| `leaderboard.json` | Liderlik tablosu kayıtları |
| `.env` | Gemini API anahtarı (`GEMINI_API_KEY`) |
| `src/ui/` | Tüm sayfa arayüzleri |
| `src/ai/` | Gemini servisi ve AI koç mantığı |
| `src/portfolio/` | Portföy durumu ve işlem yönetimi |
| `src/analysis/` | Trend analizi ve tahmin modeli |
| `src/learning/` | XP sistemi, görevler, başarımlar |
