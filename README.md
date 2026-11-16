# Koç University ELC Intermediate 07 - Midterm & Speaking Task AI Assistant 🎓

Bu proje, Koç Üniversitesi ELC Intermediate 07 sınıfı öğrencilerine **Midterm** sınavlarına ve **Speaking Task** değerlendirmelerine en yüksek verimle çalışmaları için özel olarak geliştirilmiş yapay zeka destekli bir eğitim asistanıdır.

Proje, sınıfın resmi **Skill Building Set (SBS)** müfredatını (Grammar and Beyond 3, Pathways 3, Vocabulary Practice Materials 1-5, Reading Explorer 3, Supplementary Readings ve Speaking Prompts) temel alarak çalışır.

---

## 🌟 Öne Çıkan Özellikler

1. **Midterm Sınavı Hazırlık Alanı (Chat Workspace):**
   - Cause & Effect kompozisyon mimarisi, tez cümlesi ve konu cümleleri analizi.
   - Signpost ve geçiş bağlaçları (furthermore, conversely, owing to, consequently).
   - Paraphrasing ve nominalization (sözcük türetme) çalışmaları.
   - Çok modlu destek: Ders notu, kitap sayfası fotoğrafı ve doküman yükleyerek anında satır satır geri bildirim alma.
   - Sesli konuşma (Web Speech API) ile konuşulanları anında prompt metnine dönüştürme.

2. **Speaking Task Simülatörü ve Anlık Değerlendirme:**
   - Skill Building Set içerisindeki 5 resmi konuşma konusu (veya AI ile sınırsız yeni resmi formatlı konu üretimi).
   - 1 dakikalık hazırlık ve not alma geri sayım sayacı.
   - 2 dakikalık konuşma süresi ve canlı konuşma metni (speech-to-text) transkripsiyonu.
   - CEFR B2+ Koç ELC kriterlerine göre analiz: Akıcılık & Tutarlılık, Kelime Dağarcığı (Lexical Resource), Dilbilgisi Aralığı & Doğruluğu (Grammar Accuracy), Görev Tamamlama (Task Fulfillment).
   - Güçlü yönler, geliştirilmesi gereken alanlar ve örnek model 2 dakikalık konuşma metni (isteğe bağlı sesli dinleme özelliğiyle).

3. **İnteraktif Testler & Flashcard Sistemi:**
   - SBS Vocabulary 1-5 ve Grammar Reviews 1-5'ten derlenmiş özgün sorular (Çoktan seçmeli & Gap-fill / Sentence transformation).
   - Flashcard mantığında anında doğru/yanlış geri bildirimi.
   - Yanlış veya doğru yapılan her soruda ayrıntılı kural açıklaması, akademik eş anlamlılar (synonyms) ve yaygın kullanımlar (collocations).
   - İstenilen konudan özel interaktif test üretme imkanı.

4. **Çalışma Geçmişi ve PDF İndirme:**
   - Konuşmalar ve test sonuçları tarayıcıda yerel olarak (`localStorage`) saklanır; hesap açma veya giriş yapma zorunluluğu yoktur.
   - Sol menüden (hamburger) geçmiş oturumlara erişilebilir, yeni çalışma başlatılabilir.
   - Tek tıkla tüm sohbet geçmişini, test sonuçlarını (doğru/yanlışlar ve kural açıklamaları) ve speaking değerlendirmelerini şık bir çalışma rehberi olarak **PDF formatında indirme**.

5. **Tasarım & Gizlilik:**
   - Modern "ELC Academic Glass" teması, Koç Üniversitesi INT 07 mührü/logosu.
   - Açık / Koyu tema desteği.
   - Kullanıcı arayüzünde hiçbir API anahtarı, model adı veya teknik detay görünmez; tamamen eğitim odaklıdır.

---

## 🚀 Render Üzerinde Canlıya Alma (Deployment) Adımları

Render üzerinde bu projeyi **Web Service** olarak çalıştırmak yalnızca 2 dakikanızı alır:

### Adım 1: Render Hesabınıza Giriş Yapın
1. [dashboard.render.com](https://dashboard.render.com/) adresine gidin ve giriş yapın.

### Adım 2: Yeni Web Service Oluşturun
1. Sağ üstteki **"New +"** butonuna tıklayın ve **"Web Service"** seçeneğini seçin.
2. **"Build and deploy from a Git repository"** seçeneğini seçip Next deyin.
3. GitHub reponuzu bağlayın: `https://github.com/Kgames4040/elc07ai.git` (veya Repositories listenizden `elc07ai`yi seçin).

### Adım 3: Servis Ayarlarını Yapılandırın
Aşağıdaki ayarları girin:
- **Name:** `elc07ai` (veya dilediğiniz bir isim)
- **Language / Runtime:** `Python 3`
- **Region:** Frankfurt (EU) veya dilediğiniz bir bölge
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** `Free`

### Adım 4: Ortam Değişkeni (Environment Variable) Ekleme
1. Sayfanın altındaki **"Environment Variables"** bölümünü açın.
2. **"Add Environment Variable"** butonuna tıklayın:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** `SİZİN_GEMINI_API_KEY_DEĞERİNİZ` (Google AI Studio'dan aldığınız API anahtarı)
3. **"Deploy Web Service"** butonuna tıklayın.

Birkaç dakika içinde Render bağımlılıkları yükleyecek ve sitenizi `https://elc07ai.onrender.com` benzeri ücretsiz bir URL ile yayına alacaktır!

---

## 💻 Yerel Olarak Çalıştırma (Local Development)

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. Ortam değişkeninizi ayarlayın (Windows PowerShell)
$env:GEMINI_API_KEY="AIzaSy..."

# 3. Sunucuyu başlatın
python main.py
```
Tarayıcınızdan `http://localhost:8000` adresine gidin.
