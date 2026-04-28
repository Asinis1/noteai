#  NoteAI — Akıllı Not Alma Sistemi

Yapay zeka destekli not alma, özetleme ve etiketleme uygulaması.  
**Yapay Zeka Destekli Yazılım Geliştirme** dersi dönem projesi.

---

##  Proje Hakkında

NoteAI, kullanıcıların notlarını oluşturup yönetebileceği, yapay zeka aracılığıyla otomatik özet, etiket ve anahtar kelime üretebileceği bir web uygulamasıdır.

### Özellikler

-  Kullanıcı kaydı ve JWT tabanlı kimlik doğrulama
-  Not oluşturma, düzenleme, silme
-  Klasörleme ve etiketleme sistemi
-  Notlarda arama
-  **AI ile otomatik özet üretme** (Groq / Llama 3)
-  **AI ile otomatik etiket önerisi**
-  **AI ile anahtar kelime çıkarma**

---

##  Teknoloji Altyapısı

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python, FastAPI |
| Veritabanı | SQLite + SQLAlchemy |
| Kimlik Doğrulama | JWT (python-jose) + bcrypt |
| Yapay Zeka | Groq API (Llama 3.3 70B) |
| Frontend | HTML, CSS, JavaScript |

---

##  Proje Yapısı

```
note-ai/
├── main.py                  # FastAPI ana uygulama
├── requirements.txt         # Python bağımlılıkları
├── .env                     # Gizli anahtarlar (GitHub'a yüklenmez)
├── .gitignore
├── backend/
│   ├── __init__.py
│   ├── database.py          # Veritabanı bağlantısı
│   ├── models.py            # SQLAlchemy tabloları
│   ├── schemas.py           # Pydantic şemaları
│   ├── ai_service.py        # Groq AI entegrasyonu
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Kayıt / giriş endpoint'leri
│       ├── notes.py         # Not CRUD endpoint'leri
│       └── ai.py            # AI analiz endpoint'i
└── frontend/
    └── index.html           # Tek sayfa kullanıcı arayüzü
```

---

##  Kurulum ve Çalıştırma

### Gereksinimler

- Python 3.12
- Git

---

### Adım 1 — Projeyi İndir

```bash
git clone https://github.com/Asinis1/noteai.git
cd noteai
```

---

### Adım 2 — Groq API Key Al

1. [console.groq.com](https://console.groq.com) adresine git
2. Google hesabınla giriş yap
3. **API Keys** → **Create API Key** → kopyala

---

### Adım 3 — .env Dosyası Oluştur

Proje klasöründe `.env` adında dosya oluştur:

```
GROQ_API_KEY= gsk_buraya_kendi_keyin
SECRET_KEY= herhangi_uzun_bir_yazi_123456789
DATABASE_URL= sqlite:///./smart_notes.db
```

---

### Adım 4 — Sanal Ortam Oluştur ve Kütüphaneleri Kur

```bash
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install groq
pip install bcrypt==4.0.1
```

---

### Adım 5 — Backend'i Başlat

```bash
uvicorn main:app --reload
```

`Application startup complete.` yazısını gör, terminali kapatma.

---

### Adım 6 — Frontend'i Başlat (Yeni Terminal)

```bash
cd frontend
py -m http.server 5500
```

---

### Adım 7 — Tarayıcıda Aç

```
http://localhost:5500/index.html
```

---

## Yapay Zeka Kullanımı

Bu projede **Groq API** üzerinden **Llama 3.3 70B** modeli kullanılmaktadır.

Bir nota tıklayıp **" AI ile Analiz Et"** butonuna basıldığında:

1. Not içeriği Groq API'ye gönderilir
2. Model notu analiz eder
3. Otomatik **özet**, **etiket önerileri** ve **anahtar kelimeler** üretilir
4. Sonuçlar veritabanına kaydedilir ve arayüzde gösterilir

---

##  API Endpoint'leri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/auth/register` | Kullanıcı kaydı |
| POST | `/auth/login` | Giriş ve token alma |
| GET | `/auth/me` | Aktif kullanıcı bilgisi |
| GET | `/notes/` | Tüm notları listele |
| POST | `/notes/` | Yeni not oluştur |
| PUT | `/notes/{id}` | Not güncelle |
| DELETE | `/notes/{id}` | Not sil |
| POST | `/ai/analyze/{id}` | AI ile not analiz et |

API dokümantasyonu: `http://localhost:8000/docs`

---

##  Ekip

- Proje sahipleri:
[@Asinis1](https://github.com/Asinis1)
[@rrabia-dev](https://github.com/rrabia-dev)
[@bicenaybike](https://github.com/bicenaybike)
