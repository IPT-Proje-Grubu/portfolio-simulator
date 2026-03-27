"""Educational content — all text in Turkish, targeted at complete beginners."""

from __future__ import annotations

# ── learning topics ───────────────────────────────────────────────────────────
# Each topic: icon, title, summary, tips (3 short punchy points), action_page

TOPICS: list[dict] = [
    {
        "icon": "₿",
        "title": "Kripto Para Nedir?",
        "summary": "Grafikteki canlanmayı izle — Bitcoin ile Altın'ın farkını kendin keşfet.",
        "tips": [
            ("🏦", "Bankasız para", "Hiçbir devlet veya banka kontrol etmez."),
            ("📉📈", "Yüksek oynaklık", "Bir günde ±%20 hareket görmek sıradan."),
            ("🎮", "Risk yok burada", "Sanal TL 1.000.000 ile dene, gerçek risk yok."),
        ],
        "action_label": "İşlem Sayfasına Git →",
        "action_page": 1,
        "body": [],
    },
    {
        "icon": "💼",
        "title": "Portföy Nedir?",
        "summary": "Sahip olduğun varlıkların tamamı = portföyün. Nasıl dağıttığın önemli.",
        "tips": [
            ("🧺", "Sepete koy", "Farklı varlıklar = farklı sepetler = düşük risk."),
            ("💵", "Nakit önemli", "Her zaman biraz nakit tut — fırsat düşünce hazır ol."),
            ("📊", "Takip et", "'Özet' sayfasında portföy değerin canlı görünür."),
        ],
        "action_label": "Portföyümü Gör →",
        "action_page": 0,
        "body": [],
    },
    {
        "icon": "⇄",
        "title": "Alım / Satım Nasıl Çalışır?",
        "summary": "3 adım: Varlık seç → Miktar gir → Onayla. Hepsi bu.",
        "tips": [
            ("1️⃣", "Tıkla", "'İşlem' sayfasında sol listeden bir varlığa tıkla."),
            ("2️⃣", "Gir", "Miktar alanını doldur, toplam otomatik hesaplanır."),
            ("3️⃣", "Onayla", "'İŞLEM GERÇEKLEŞTIR' butonuna bas — bitti!"),
        ],
        "action_label": "Şimdi Dene →",
        "action_page": 1,
        "body": [],
    },
    {
        "icon": "📈",
        "title": "Kar ve Zarar (K/Z)",
        "summary": "Aşağıdaki hesaplayıcıyla formülü bizzat dene — sayıları değiştir.",
        "tips": [
            ("🔢", "Basit formül", "(Güncel − Alış) × Miktar = K/Z"),
            ("📄", "Kâğıt kayıp", "Satmadıkça kayıp gerçekleşmez — sadece 'kâğıt üzeri'."),
            ("🎨", "Renk kodu", "Yeşil = kâr, Kırmızı = zararda pozisyon."),
        ],
        "action_label": "Portföy K/Z'ye Git →",
        "action_page": 0,
        "body": [],
    },
    {
        "icon": "〜",
        "title": "Volatilite ve Risk",
        "summary": "Çubuk ne kadar uzunsa, fiyat o kadar çok zıplar. Hangisi seni rahatlatır?",
        "tips": [
            ("😤", "Panikle satma", "Düşüş görünce satmak en yaygın yatırımcı hatasıdır."),
            ("🛡️", "Çeşitlendirme", "Kripto + hisse + altın karışımı riski dengeler."),
            ("🐢", "Altın & BIST", "Başlamak için en düşük riskli seçenekler."),
        ],
        "action_label": "Varlıkları Karşılaştır →",
        "action_page": 1,
        "body": [],
    },
    {
        "icon": "⭐",
        "title": "Varlık Rehberi",
        "summary": "Her çubuk bir varlık. Renge bak, riske karar ver.",
        "tips": [
            ("₿", "BTC & ETH", "En büyük, en likit kriptolar. Çok yüksek risk."),
            ("🍎", "Hisseler", "AAPL, MSFT, NVDA — kriptodan daha az oynak."),
            ("🥇", "GOLD & BIST", "Güvenli liman. Düşük kazanç, düşük risk."),
        ],
        "action_label": "İşlem Sayfasına Git →",
        "action_page": 1,
        "body": [],
    },
    {
        "icon": "💡",
        "title": "Başlangıç Stratejileri",
        "summary": "Kaydırıcıları oynat — DCA ile toplu alım arasındaki farkı gör.",
        "tips": [
            ("📅", "DCA", "Her ay sabit miktar al → ortalama maliyeti düşür."),
            ("🤚", "HODL", "4+ yıl tut → tarihsel verilere göre genelde kârlı."),
            ("😌", "Duygusuz kal", "FOMO ve panik = en pahalı yatırım hataları."),
        ],
        "action_label": "İşlem Yap →",
        "action_page": 1,
        "body": [],
    },
]

# ── glossary ──────────────────────────────────────────────────────────────────

GLOSSARY: list[dict] = [
    {"term": "Portföy",          "def": "Sahip olunan tüm yatırım araçlarının bütünü."},
    {"term": "Volatilite",       "def": "Fiyatların ne kadar hızlı ve büyük değiştiğinin ölçüsü. Yüksek = riskli."},
    {"term": "Ortalama Maliyet", "def": "Aynı varlığı farklı fiyatlardan alındığında hesaplanan ağırlıklı ortalama."},
    {"term": "K/Z (P/L)",        "def": "Kar / Zarar. Yatırımın güncel değeri ile maliyeti arasındaki fark."},
    {"term": "Gerçekleşmiş K/Z", "def": "Satış sonrası kesinleşen kazanç veya kayıp."},
    {"term": "Gerçekleşmemiş K/Z","def": "Hâlâ elde tutulan varlığın kâğıt üzerindeki kar/zararı."},
    {"term": "Piyasa Fiyatı",    "def": "Bir varlığın anlık alınıp satılabileceği fiyat."},
    {"term": "Blokzincir",       "def": "Kripto işlemlerinin şeffaf ve değiştirilemez şekilde kaydedildiği dağıtık defter."},
    {"term": "DCA",              "def": "Dollar-Cost Averaging — düzenli ve sabit miktarda alım stratejisi."},
    {"term": "HODL",             "def": "Uzun vadeli tutma stratejisi; kısa vadeli dalgalanmalara aldırmamak."},
    {"term": "FOMO",             "def": "Fear Of Missing Out — fırsatı kaçırma korkusuyla aceleci karar vermek."},
    {"term": "FUD",              "def": "Fear, Uncertainty, Doubt — piyasada panik yaratmak amaçlı olumsuz haberler."},
    {"term": "Altcoin",          "def": "Bitcoin dışındaki tüm kripto paralar (ETH, BNB, SOL vb.)."},
    {"term": "Borsa",            "def": "Kripto paraların alınıp satıldığı platform (Binance, Coinbase vb.)."},
    {"term": "Cüzdan",           "def": "Kripto paraların saklandığı dijital depolama aracı."},
    {"term": "Çeşitlendirme",    "def": "Riski dağıtmak için farklı varlıklara yatırım yapma stratejisi."},
    {"term": "Piyasa Değeri",    "def": "Toplam dolaşımdaki arz × fiyat. Varlığın büyüklüğünü gösterir."},
    {"term": "Likidite",         "def": "Bir varlığın fiyatını çok etkilemeden ne kadar kolay alınıp satılabileceği."},
]

# ── asset educational info ────────────────────────────────────────────────────

ASSET_INFO: dict[str, dict] = {
    "BTC":  {"risk": "Çok Yüksek", "risk_level": 5, "desc": "Bitcoin — dünyanın ilk kripto parası. 'Dijital altın' olarak bilinir."},
    "ETH":  {"risk": "Çok Yüksek", "risk_level": 5, "desc": "Ethereum — akıllı sözleşmeler ve DeFi platformu."},
    "BNB":  {"risk": "Yüksek",     "risk_level": 4, "desc": "Binance'in kripto parası. Borsa işlem ücretlerinde indirim sağlar."},
    "SOL":  {"risk": "Çok Yüksek", "risk_level": 5, "desc": "Solana — hızlı ve ucuz işlemler sunan blokzincir."},
    "AAPL": {"risk": "Orta",       "risk_level": 2, "desc": "Apple Inc. — dünyanın en yüksek piyasa değerli şirketlerinden biri."},
    "MSFT": {"risk": "Orta",       "risk_level": 2, "desc": "Microsoft — yazılım ve bulut bilişim devi."},
    "NVDA": {"risk": "Yüksek",     "risk_level": 4, "desc": "Nvidia — yapay zeka ve GPU sektörünün lideri."},
    "TSLA": {"risk": "Yüksek",     "risk_level": 4, "desc": "Tesla — elektrikli araç ve enerji şirketi."},
    "GOOG": {"risk": "Orta",       "risk_level": 3, "desc": "Alphabet (Google) — arama ve reklam teknolojisi."},
    "AMZN": {"risk": "Orta",       "risk_level": 3, "desc": "Amazon — e-ticaret ve bulut altyapısı (AWS)."},
    "GOLD": {"risk": "Düşük",      "risk_level": 1, "desc": "Altın — tarihin en güvenli yatırım araçlarından biri."},
    "BIST": {"risk": "Düşük",      "risk_level": 1, "desc": "BIST 100 — Türkiye'nin en büyük 100 şirket endeksi."},
}

# ── beginner tips (shown randomly in status bar) ──────────────────────────────

TIPS: list[str] = [
    "İPUCU: Piyasayı bir süre gözlemleyin. Fiyatların nasıl hareket ettiğini anlamak için acele etmeyin.",
    "İPUCU: Altın (GOLD) ve BIST100 en düşük riskli varlıklardır — başlamak için iyi bir yer!",
    "İPUCU: Asla tüm nakdinizi tek bir varlığa yatırmayın. Çeşitlendirme riski azaltır.",
    "İPUCU: K/Z değeri kırmızı görünse endişelenmeyin — bu bir simülasyon, öğrenmek için buradayız.",
    "İPUCU: 'Öğren' sayfasında her kavramın detaylı açıklamasını bulabilirsiniz.",
    "İPUCU: BTC ve ETH en likit kripto paralardır — her zaman alıcı ve satıcı bulunur.",
    "İPUCU: Piyasa fiyatı her 3 saniyede bir güncelleniyor. Gerçek piyasalarda bu anlık olur!",
    "İPUCU: İşlem geçmişinizi inceleyerek hangi kararların iyi sonuç verdiğini analiz edin.",
    "İPUCU: 'Senaryo Simülasyonu' ile mevcut portföyünüzün farklı tarihlerdeki performansını test edin.",
    "İPUCU: TSLA ve SOL en volatil varlıklar arasında — küçük miktarlarla deneyin.",
]

# ── tutorial steps ────────────────────────────────────────────────────────────

TUTORIAL_STEPS: list[dict] = [
    {
        "id":    "view_market",
        "title": "Piyasayı inceleyin",
        "desc":  "'İşlem' sayfasına gidin ve fiyatların değişimini izleyin.",
        "page":  1,
    },
    {
        "id":    "first_buy",
        "title": "İlk alımınızı yapın",
        "desc":  "Bir varlığa tıklayıp miktar girerek ilk işleminizi gerçekleştirin.",
        "page":  1,
    },
    {
        "id":    "check_portfolio",
        "title": "Portföyünüzü izleyin",
        "desc":  "'Özet' sayfasında K/Z değerinin değişimini gözlemleyin.",
        "page":  0,
    },
    {
        "id":    "first_sell",
        "title": "İlk satışınızı yapın",
        "desc":  "SATIŞ moduna geçerek elinizdeki varlığın bir kısmını satın.",
        "page":  1,
    },
    {
        "id":    "check_history",
        "title": "Geçmişi inceleyin",
        "desc":  "'Geçmiş' sayfasında tüm işlemlerinizi görün.",
        "page":  2,
    },
    {
        "id":    "run_analysis",
        "title": "Senaryo analizi çalıştırın",
        "desc":  "'Analiz' sayfasından portföyünüzü projekte edin.",
        "page":  4,
    },
]
