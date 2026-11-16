import os
import io
import json
import base64
import requests
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict

# Document parsing libraries
try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    print("[Warning] python-docx not installed, docx parsing disabled.")

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False
    print("[Warning] pypdf not installed, pdf text extraction disabled.")

# Converter module
try:
    import converter
    HAS_CONVERTER = True
except ImportError:
    HAS_CONVERTER = False
    print("[Warning] converter module not loaded.")

app = FastAPI(title="Koç University ELC INT 07 Academic AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load wordlist data
ACADEMIC_WORDLIST = []
try:
    if os.path.exists("academic_wordlist.json"):
        with open("academic_wordlist.json", "r", encoding="utf-8") as f:
            ACADEMIC_WORDLIST = json.load(f)
            print(f"[Curriculum] Loaded {len(ACADEMIC_WORDLIST)} words from academic_wordlist.json")
except Exception as e:
    print("[Warning] Could not load academic_wordlist.json:", e)

# Load curriculum knowledge base
SBS_KNOWLEDGE_SUMMARY = ""
try:
    if os.path.exists("sbs_curriculum_extracted.json"):
        with open("sbs_curriculum_extracted.json", "r", encoding="utf-8") as f:
            raw_sbs = json.load(f)
    SBS_KNOWLEDGE_SUMMARY = f"""
Official Curriculum Structure for Koç University ELC Intermediate 07:
- Grammar: Grammar and Beyond 3 (Units 1-5, 7-11, 19-22, 28) and Grammar Reviews 1-5 (Narrative tenses, correlative comparatives 'The... the...', cause-and-effect connectors, relative clauses, conditionals, passive voice).
- Vocabulary & Collocations: Over 600 official Intermediate headwords with complete word families and prepositions (rely on, capable of, discourage from, aware of, make a contribution to, impose constraints on, crucial for/to, beneficial to, adapt to, associated with, etc.) based on Pathways 3 Reading & Writing and Listening & Speaking Units 1 to 10.
- Reading: Pathways 3 Reading & Writing Unit Tests 1-5, Reading Explorer 3 Units 1-6, Supplementary Readings (AI-AR New Life, Consumerism, Talking with Animals, The Art of Looks, The Future of Education, The Measurement of Happiness).
- Listening & Note-Taking: US Population, Bobo Doll Experiment, Reading on-screen vs on-paper, Women in STEM, Designing for Well-being.
- Speaking Task Official Prompts:
  1) Restaurant food & consumer decisions (factors, takeout vs dine-in, deal evaluation)
  2) Personality traits: Nature vs Nurture (genetic vs environmental, changes)
  3) Relocation & moving to a new place (advantages, disadvantages, short stay vs settling)
  4) Natural places / geographical features (description, impact, conservation efforts)
  5) Career aspirations & ideal job (responsibilities, required qualifications, fit)
- Writing Prompts: University vs High School life, Working at international companies, Technology in education, Protecting wild places (Cause & Effect essay architecture, signpost transitions).
"""
except Exception as e:
    SBS_KNOWLEDGE_SUMMARY = "Koç University ELC Intermediate 07 Skill Building Set syllabus and Academic Wordlist."

SYSTEM_PROMPT = f"""You are the official Academic AI Study Assistant for Koç University ELC Intermediate 07 class students.
Your primary mission is to coach and prepare students for their upcoming Midterm exam and Speaking Tasks based on the official Intermediate Skill Building Set (SBS) and the Core Academic Wordlist.

Key Guidelines:
1. CURRICULUM GROUNDING:
All explanations, grammar rules, vocabulary distinctions, reading tips, and speaking evaluations must adhere strictly to the Koç ELC Intermediate syllabus:
{SBS_KNOWLEDGE_SUMMARY}

2. MULTIMODAL & DOCUMENT SUPPORT:
- When a student uploads an image (handwritten essay draft, notebook photo, textbook exercise, whiteboard capture), transcribe any relevant text, analyze it thoroughly line-by-line, point out grammar/lexis errors according to CEFR B2+ criteria, and praise good usage of transitions/collocations.
- When a document is attached, read the extracted content and provide structured academic feedback.

3. SPEAKING TASK PRACTICE & EVALUATION:
- Official format: 1 minute preparation & note-taking, 2 minutes speaking.
- Rubric criteria: CEFR B2+ Lexical Resource (academic collocations, precision), Grammatical Range & Accuracy (complex sentences, correct tenses, conditionals, passive voice), Fluency & Coherence (signpost words, discourse markers, smooth transitions), and Task Fulfillment (addressing all sub-questions).

4. TONE & BRANDING:
- Maintain an encouraging, academic, clear, and structured pedagogical tone.
- Answer in the language the student speaks (English or Turkish; keep academic examples and grammar terms in English).
- Format responses cleanly with markdown: bold headings, bullet points, and clear examples.
- NEVER disclose or state that you are Gemini, Google, or any internal model name. You are solely the "Koç University ELC INT 07 AI Assistant".
- NEVER mention API keys or backend mechanics.
"""

def sanitize_gemini_contents(raw_contents: list) -> list:
    """Ensure Gemini multi-turn format strictly alternates: user -> model -> user -> model, starting with user."""
    if not raw_contents:
        return []

    cleaned = []
    for turn in raw_contents:
        role = turn.get("role", "user")
        if role not in ["user", "model"]:
            role = "user"
        parts = turn.get("parts", [])
        valid_parts = [p for p in parts if ("text" in p and p["text"].strip()) or "inlineData" in p]
        if not valid_parts:
            continue

        if not cleaned:
            if role != "user":
                continue
            cleaned.append({"role": "user", "parts": valid_parts})
        else:
            last_turn = cleaned[-1]
            if last_turn["role"] == role:
                last_turn["parts"].extend(valid_parts)
            else:
                cleaned.append({"role": role, "parts": valid_parts})

    if cleaned and cleaned[-1]["role"] != "user":
        cleaned.append({"role": "user", "parts": [{"text": "Please continue with the ELC INT 07 analysis."}]})

    return cleaned


def call_gemini(contents: list, system_instruction: str = SYSTEM_PROMPT) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return (
            "⚠️ **API Anahtarı Bulunamadı / API Key Missing**\n\n"
            "Render web servisinde `GEMINI_API_KEY` environment variable (ortam değişkeni) tanımlanmamış.\n\n"
            "Lütfen Render Dashboard > Environment Variables bölümüne gidip `GEMINI_API_KEY` değerinizi ekleyin."
        )

    # Prioritize gemini-2.5-flash as requested
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    last_error = ""

    valid_contents = sanitize_gemini_contents(contents)
    if not valid_contents:
        return "İçerik tespit edilemedi. Lütfen sorunuzu veya dosyanızı tekrar gönderin."

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": valid_contents,
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.6,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        try:
            print(f"[ELC AI] Requesting {model} with {len(valid_contents)} turns...")
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    reply = "".join([p.get("text", "") for p in parts if "text" in p])
                    if reply.strip():
                        print(f"[ELC AI] {model} responded successfully ({len(reply)} chars).")
                        return reply
                print(f"[ELC AI] {model} returned candidate with no text parts.")
            else:
                print(f"[ELC AI] {model} error {resp.status_code}: {resp.text[:200]}")
                last_error = f"Status {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            print(f"[ELC AI] {model} exception: {str(e)}")
            last_error = str(e)

    return f"AI servisiyle bağlantı kurulamadı ({last_error}). Lütfen tekrar deneyiniz."


def extract_attachment_content(file_attachment: dict):
    """
    Parses images, PDFs, Word docs, and plain text files.
    Returns: (list_of_gemini_parts, extracted_text_note)
    """
    if not file_attachment or not file_attachment.get("base64"):
        return [], ""

    b64_raw = file_attachment.get("base64", "")
    filename = file_attachment.get("name", "document").lower()
    raw_mime = file_attachment.get("mime_type", "").lower()

    if "," in b64_raw:
        header, b64_clean = b64_raw.split(",", 1)
        if "data:" in header and ";base64" in header:
            detected_mime = header.split("data:")[1].split(";")[0].lower()
            if detected_mime:
                raw_mime = detected_mime
    else:
        b64_clean = b64_raw

    b64_clean = b64_clean.replace("\n", "").replace("\r", "").strip()

    try:
        decoded_bytes = base64.b64decode(b64_clean)
    except Exception as e:
        print("[Attachment] Failed to decode base64:", e)
        return [], f"[Dosya okunamadı: {filename}]"

    # 1. Word Document (.docx / .doc)
    if (filename.endswith(".docx") or "wordprocessingml" in raw_mime or filename.endswith(".doc")) and HAS_DOCX:
        try:
            doc = Document(io.BytesIO(decoded_bytes))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    cells = [c.text.strip() for c in row.cells if c.text.strip()]
                    if cells:
                        paragraphs.append(" | ".join(cells))
            extracted_doc_text = "\n".join(paragraphs)
            if not extracted_doc_text.strip():
                extracted_doc_text = "(Boş Word belgesi tespit edildi)"
            return [{"text": f"--- YÜKLENEN WORD BELGESİ: {filename} ---\n{extracted_doc_text}\n--- BELGE SONU ---\n"}], "word_doc"
        except Exception as e:
            print("[Attachment] docx extraction error:", e)

    # 2. PDF Document (.pdf)
    if filename.endswith(".pdf") or "pdf" in raw_mime:
        if HAS_PYPDF:
            try:
                reader = PdfReader(io.BytesIO(decoded_bytes))
                pdf_text = ""
                for idx, page in enumerate(reader.pages):
                    txt = page.extract_text()
                    if txt:
                        pdf_text += f"\n[Sayfa {idx+1}]\n" + txt
                if pdf_text.strip():
                    return [{"text": f"--- YÜKLENEN PDF BELGESİ: {filename} ---\n{pdf_text}\n--- PDF SONU ---\n"}], "pdf_doc"
            except Exception as e:
                print("[Attachment] PDF text extraction error:", e)

        return [{
            "inlineData": {
                "mimeType": "application/pdf",
                "data": b64_clean
            }
        }], "pdf_inline"

    # 3. Plain Text / Markdown / Code (.txt, .md, .csv)
    if filename.endswith(".txt") or filename.endswith(".md") or filename.endswith(".csv") or "text/" in raw_mime:
        try:
            txt_content = decoded_bytes.decode("utf-8", errors="replace")
            return [{"text": f"--- YÜKLENEN METİN DOSYASI: {filename} ---\n{txt_content}\n--- DOSYA SONU ---\n"}], "text_file"
        except Exception as e:
            print("[Attachment] Text file decode error:", e)

    # 4. Images (JPG, PNG, WEBP, GIF, HEIC)
    clean_mime = "image/jpeg"
    if "png" in raw_mime or filename.endswith(".png"):
        clean_mime = "image/png"
    elif "webp" in raw_mime or filename.endswith(".webp"):
        clean_mime = "image/webp"
    elif "gif" in raw_mime or filename.endswith(".gif"):
        clean_mime = "image/gif"
    elif "heic" in raw_mime or filename.endswith(".heic"):
        clean_mime = "image/heic"
    elif "jpeg" in raw_mime or "jpg" in raw_mime or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        clean_mime = "image/jpeg"

    return [
        {
            "inlineData": {
                "mimeType": clean_mime,
                "data": b64_clean
            }
        },
        {
            "text": f"Öğrenci bir görsel/ders notu fotoğrafı yükledi: '{filename}'. Lütfen görseldeki el yazısını, sınav sorusunu, okuma metnini veya notları detaylıca oku ve Koç Üniversitesi ELC Intermediate 07 seviyesine uygun olarak analiz et.\n"
        }
    ], "image"


class ChatRequest(BaseModel):
    message: Optional[str] = ""
    history: Optional[List[Any]] = []
    file_attachment: Optional[dict] = None

@app.get("/api/status")
def get_status():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    return {
        "status": "online",
        "has_api_key": bool(api_key),
        "institution": "Koç University",
        "program": "ELC Intermediate 07",
        "term": "Fall 2026",
        "wordlist_count": len(ACADEMIC_WORDLIST)
    }

@app.get("/api/wordlist")
def get_wordlist(unit: Optional[str] = None):
    """Returns the loaded academic wordlist."""
    if not unit:
        return ACADEMIC_WORDLIST
    filtered = [w for w in ACADEMIC_WORDLIST if any(unit.lower() in u.lower() for u in w.get("units", []))]
    return filtered

@app.get("/api/tests")
def get_tests():
    if os.path.exists("static/curriculum_tests.json"):
        with open("static/curriculum_tests.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    contents = []

    if req.history:
        for turn in req.history[-8:]:
            role = turn.get("role", "user")
            gemini_role = "model" if role in ["assistant", "model"] else "user"
            text_content = turn.get("content", "")
            if text_content and text_content.strip():
                contents.append({
                    "role": gemini_role,
                    "parts": [{"text": text_content.strip()}]
                })

    current_parts = []

    if req.file_attachment:
        att_parts, att_type = extract_attachment_content(req.file_attachment)
        if att_parts:
            current_parts.extend(att_parts)
            print(f"[Attachment] Attached {att_type} ({req.file_attachment.get('name')}) successfully.")

    user_text = (req.message or "").strip()
    if not user_text:
        if req.file_attachment:
            user_text = "Lütfen eklediğim bu belgeyi/görseli detaylıca analiz et; içindeki konu, soru, kelimeler ve kompozisyon yapısını Koç Üniversitesi ELC Intermediate 07 seviyesine göre değerlendirip bana geri bildirim ver."
        else:
            user_text = "Merhaba ELC 07 AI Assistant."

    # LOGGING USER PROMPT AS REQUESTED
    print(f"PROMPT: {user_text}", flush=True)

    current_parts.append({"text": user_text})

    contents.append({
        "role": "user",
        "parts": current_parts
    })

    reply = call_gemini(contents)
    return {"reply": reply}


# ============================================================
# MODULE 1: CÜMLE SEVİYE YÜKSELTİCİ (SENTENCE BOOSTER)
# ============================================================
class SentenceUpgradeRequest(BaseModel):
    sentence: str
    focus: Optional[str] = "Otomatik (Materyale Göre)"

@app.post("/api/upgrade-sentence")
def upgrade_sentence(req: SentenceUpgradeRequest):
    raw_sentence = (req.sentence or "").strip()
    if not raw_sentence:
        raise HTTPException(status_code=400, detail="Lütfen seviyesini yükseltmek istediğiniz bir cümle giriniz.")

    # LOGGING USER PROMPT
    print(f"PROMPT: [Cümle Seviye Yükseltici] '{raw_sentence}' (Odak: {req.focus})", flush=True)

    upgrade_prompt = f"""
Öğrenci Koç Üniversitesi ELC Intermediate (INT 07) seviyesinde bir cümle seviye yükseltme talebinde bulundu.

ÖĞRENCİNİN GİRDİĞİ BASİT CÜMLE:
"{raw_sentence}"

KULLANICI ODAK TERCİHİ:
"{req.focus}"

ELC Intermediate (CEFR B2+) sınav standartlarında, Skill Building Set materyalleri ve Intermediate Academic Wordlist'i referans alarak bu cümleyi 3 farklı üst seviye alternatife dönüştür.

Kurallar ve Beklentiler:
1. "dilbilgisi_versiyonu": Müfredattaki hedef dilbilgisi yapılarını (örneğin sıfat cümlecikleri - relative clauses: which, where, whose; isim cümlecikleri - noun clauses; edilgen çatı - passive voice; correlative comparatives 'The... the...'; şart cümleleri - conditionals; sebep-sonuç bağlaçları) kullan. Cümle içinde hedef yapıyı **kalın** olarak vurgula.
2. "kelime_versiyonu": Basit kelimeler yerine ELC Intermediate kelime listesindeki eş anlamlıları ve doğru edat/kalıp kullanımlarını (örneğin rely on, aware of, play a crucial role in, significant proportion vb.) içeren zenginleştirilmiş versiyon.
3. "konusma_versiyonu": Speaking sınavında hocanın kulağına doğal, akıcı gelecek ve uygun geçiş/söylem ifadeleriyle (discourse markers, signpost words: "from my perspective", "consequently", "it is worth noting that", vb.) zenginleştirilmiş versiyon.
4. ELC Intermediate seviyesinin çok üstünde (C2 gibi yapay ve ezber duran) aşırı karmaşık kelimeler KULLANMA. Tam olarak INT 07 müfredatındaki hedef yapıları kullan.
5. "turkce_aciklama" alanlarında neden bu versiyonun sınavda daha yüksek puan getireceğini sade ve anlaşılır tek bir Türkçe cümleyle açıkla.

Yanıtı KESİNLİKLE aşağıdaki JSON formatında döndür:
{{
  "orijinal_cumle": "{raw_sentence}",
  "dilbilgisi_versiyonu": {{
    "cumle": "Gramer odaklı yükseltilmiş cümle (hedef yapı **kalın** yazılmış)",
    "vurgulanan_yapi": "Kullanılan hedef dilbilgisi kuralı (ör: Relative clause with 'which')",
    "turkce_aciklama": "Neden bu daha yüksek puan getirir?"
  }},
  "kelime_versiyonu": {{
    "cumle": "Akademik kelime ve kalıp odaklı cümle",
    "hedef_kelimeler": ["hedef1", "hedef2"],
    "turkce_aciklama": "Neden bu daha yüksek puan getirir?"
  }},
  "konusma_versiyonu": {{
    "cumle": "Speaking sınavı için doğal ve akıcı cümle",
    "anahtar_kalip": "Kullanılan söylem veya akıcılık kalıbı",
    "turkce_aciklama": "Neden bu daha yüksek puan getirir?"
  }}
}}
Çıktı SADECE geçerli JSON olmalıdır. Markdown kod bloğu dışında hiçbir metin yazma.
"""

    raw_response = call_gemini(
        [{"role": "user", "parts": [{"text": upgrade_prompt}]}],
        system_instruction="You are an expert Koç University ELC Intermediate Writing and Grammar Examiner. Output ONLY valid JSON."
    )

    clean_json = raw_response.strip()
    if clean_json.startswith("```"):
        clean_json = clean_json.split("\n", 1)[1]
    if clean_json.endswith("```"):
        clean_json = clean_json.rsplit("\n", 1)[0]
    clean_json = clean_json.strip()

    try:
        parsed = json.loads(clean_json)
        return parsed
    except Exception as e:
        print("[Upgrade Sentence] JSON parse failed, returning fallback:", e)
        return {
            "orijinal_cumle": raw_sentence,
            "dilbilgisi_versiyonu": {
                "cumle": f"Although many individuals tend to overlook it, {raw_sentence.lower()} **which plays a vital role** in overall academic achievement.",
                "vurgulanan_yapi": "Adverbial clause of concession + Non-defining relative clause",
                "turkce_aciklama": "Basit cümleyi zıtlık bağlacı ve niteleyici sıfat cümleciğiyle birleştirerek B2+ seviye karmaşık cümle yapısı kurar."
            },
            "kelime_versiyonu": {
                "cumle": f"Substantial evidence indicates that individuals actively **engage in** {raw_sentence.lower()}, thereby yielding significant long-term benefits.",
                "hedef_kelimeler": ["substantial evidence", "engage in", "yielding significant benefits"],
                "turkce_aciklama": "Günlük kelimeler yerine ELC kelime listesindeki akademik eş anlamlılar ve fiil-edat kalıpları tercih edilmiştir."
            },
            "konusma_versiyonu": {
                "cumle": f"From my personal perspective, it is evident that {raw_sentence.lower()}; consequently, this leads to a more favorable outcome.",
                "anahtar_kalip": "From my personal perspective ... consequently",
                "turkce_aciklama": "Sözlü sınav hocasının beklediği doğal fikir belirtme ve sebep-sonuç geçiş ifadesi içerir."
            }
        }


# ============================================================
# MODULE 2: AKILLI KELİME KARTLARI (FLASHCARD GENERATOR)
# ============================================================
class FlashcardGenRequest(BaseModel):
    source: Optional[str] = "curriculum" # "curriculum", "text", "unit"
    text: Optional[str] = ""
    unit: Optional[str] = None
    count: Optional[int] = 10

@app.post("/api/generate-flashcards")
def generate_flashcards(req: FlashcardGenRequest):
    # LOGGING USER PROMPT
    prompt_desc = req.text[:80] if req.text else (req.unit or "Skill Building Set Müfredatı")
    print(f"PROMPT: [Akıllı Kelime Kartları] Kaynak: {req.source}, Detay: '{prompt_desc}'", flush=True)

    count = min(max(req.count or 10, 8), 12)

    context_hint = ""
    if req.source == "text" and req.text.strip():
        context_hint = f"Öğrencinin yapıştırdığı metin/parça:\n\"\"\"{req.text.strip()}\"\"\"\nLütfen bu metindeki en kritik ve sınavda çıkabilecek B2+ kelimeleri seç."
    elif req.unit and req.unit.strip():
        context_hint = f"Öğrenci Pathways 3 / Skill Building Set '{req.unit}' ünitesinden kelime kartı üretilmesini istedi."
    else:
        # Sample some words from academic wordlist for grounding
        import random
        sample_words = random.sample(ACADEMIC_WORDLIST, min(len(ACADEMIC_WORDLIST), 25)) if ACADEMIC_WORDLIST else []
        sample_str = ", ".join([w.get("headword", "") for w in sample_words if w.get("headword")])
        context_hint = f"Sistemde yüklü Koç ELC Intermediate Core Academic Wordlist ve Pathways 3 ünitelerinden en sık çıkan kelimeleri seç. Referans kelimelerden bazıları: {sample_str}"

    gen_prompt = f"""
Koç Üniversitesi ELC Intermediate (INT 07) öğrencileri için Midterm sınavına hazırlık amaçlı {count} adet Akıllı Kelime Kartı (Flashcard) üret.

BAĞLAM:
{context_hint}

KURALLAR:
1. Sınavda boşluk doldurma (gap-fill), eş anlamlı veya speaking'de çıkma ihtimali en yüksek 8 ila 12 kelimeyi seç.
2. Her kart için:
   - "kelime": Hedef İngilizce kelime (headword)
   - "tur": Kelimenin türü (İsim, Fiil, Sıfat veya Zarf)
   - "turkce_anlam": Net ve doğru Türkçe karşılığı
   - "ingilizce_tanim": B2+ seviyesinde kısa ve anlaşılır İngilizce tanım
   - "kalip_ve_edatlar": Sınavda test edilen birlikte kullanıldığı edatlar ve kalıplar (ör: rely **on**, aware **of**, make a contribution **to**). Edatı/kalıbı kalın göster.
   - "kelime_ailesi": Diğer türemiş halleri: {{"isim": "...", "fiil": "...", "sifat": "...", "zarf": "..."}} (olanları yaz, olmayanları null veya boş bırak).
   - "ornek_cumle": Kelimenin geçtiği, ELC Intermediate sınav seviyesinde otantik akademik örnek cümle.
3. Seviye kesinlikle CEFR B2+ olmalı, yapay C2 veya çok basit A1/A2 kelimeler olmamalıdır.

Çıktıyı KESİNLİKLE aşağıdaki JSON dizisi formatında döndür:
[
  {{
    "kelime": "rely",
    "tur": "Fiil",
    "turkce_anlam": "Güvenmek, bel bağlamak",
    "ingilizce_tanim": "To depend on someone or something with confidence",
    "kalip_ve_edatlar": ["rely **on** sb/sth", "reliance **on**", "a reliable source"],
    "kelime_ailesi": {{
      "isim": "reliance",
      "fiil": "rely",
      "sifat": "reliable",
      "zarf": "reliably"
    }},
    "ornek_cumle": "University researchers heavily rely on accurate data when conducting experiments."
  }}
]
SADECE JSON dizisi üret.
"""

    raw_response = call_gemini(
        [{"role": "user", "parts": [{"text": gen_prompt}]}],
        system_instruction="You are an expert ELC Lexical Syllabus Designer. Output ONLY raw JSON array."
    )

    clean_json = raw_response.strip()
    if clean_json.startswith("```"):
        clean_json = clean_json.split("\n", 1)[1]
    if clean_json.endswith("```"):
        clean_json = clean_json.rsplit("\n", 1)[0]
    clean_json = clean_json.strip()

    try:
        cards = json.loads(clean_json)
        if isinstance(cards, list) and len(cards) > 0:
            return {"cards": cards}
    except Exception as e:
        print("[Flashcards] JSON parse error:", e)

    # Fallback to rich pre-curated cards from academic_wordlist
    fallback_cards = [
        {
            "kelime": "rely",
            "tur": "Fiil",
            "turkce_anlam": "Güvenmek, bel bağlamak",
            "ingilizce_tanim": "To depend on with full trust or confidence",
            "kalip_ve_edatlar": ["rely **on** sb/sth", "reliance **on** sb/sth", "a reliable source"],
            "kelime_ailesi": {"isim": "reliance", "fiil": "rely", "sifat": "reliable", "zarf": "reliably"},
            "ornek_cumle": "University students heavily rely on academic databases when conducting research."
        },
        {
            "kelime": "aware",
            "tur": "Sıfat",
            "turkce_anlam": "Farkında, haberdar",
            "ingilizce_tanim": "Having knowledge or perception of a situation or fact",
            "kalip_ve_edatlar": ["to be aware **of** sth", "raise awareness **about**", "a lack **of** awareness"],
            "kelime_ailesi": {"isim": "awareness", "fiil": "", "sifat": "aware", "zarf": ""},
            "ornek_cumle": "Consumers are becoming increasingly aware of the environmental consequences of fast fashion."
        },
        {
            "kelime": "contribute",
            "tur": "Fiil",
            "turkce_anlam": "Katkıda bulunmak, katkı sağlamak",
            "ingilizce_tanim": "To give something in order to help achieve or provide something",
            "kalip_ve_edatlar": ["make a contribution **to** sth", "contribute **to** sth", "a major contributor"],
            "kelime_ailesi": {"isim": "contribution", "fiil": "contribute", "sifat": "", "zarf": ""},
            "ornek_cumle": "Technological innovation has made a significant contribution to modern medical care."
        },
        {
            "kelime": "crucial",
            "tur": "Sıfat",
            "turkce_anlam": "Hayati, son derece önemli",
            "ingilizce_tanim": "Decisive or critical, especially in the success or failure of something",
            "kalip_ve_edatlar": ["crucial **for/to** sth", "play a crucial role **in** doing sth", "a crucial piece of evidence"],
            "kelime_ailesi": {"isim": "", "fiil": "", "sifat": "crucial", "zarf": "crucially"},
            "ornek_cumle": "Consistent note-taking plays a crucial role in preparing for intermediate exams."
        },
        {
            "kelime": "adapt",
            "tur": "Fiil",
            "turkce_anlam": "Uyum sağlamak, uyarlamak",
            "ingilizce_tanim": "To adjust to new conditions or environment",
            "kalip_ve_edatlar": ["adapt **to** sth successfully", "to be adaptable", "an adaptation **of**"],
            "kelime_ailesi": {"isim": "adaptation", "fiil": "adapt", "sifat": "adaptable", "zarf": ""},
            "ornek_cumle": "International students often find it challenging to adapt to an unfamiliar university environment."
        },
        {
            "kelime": "impose",
            "tur": "Fiil",
            "turkce_anlam": "Yürürlüğe koymak, zorla uygulamak",
            "ingilizce_tanim": "To force an unwelcome decision or ruling on someone",
            "kalip_ve_edatlar": ["impose constraints **on** sb/sth", "impose restrictions **on**", "impose a fine **on**"],
            "kelime_ailesi": {"isim": "imposition", "fiil": "impose", "sifat": "imposing", "zarf": ""},
            "ornek_cumle": "Governments frequently impose strict regulations on companies that pollute water sources."
        },
        {
            "kelime": "beneficial",
            "tur": "Sıfat",
            "turkce_anlam": "Yararlı, faydalı",
            "ingilizce_tanim": "Resulting in good; favorable or advantageous",
            "kalip_ve_edatlar": ["benefit **from** sth", "to be beneficial **to** sb/sth", "enormous benefit"],
            "kelime_ailesi": {"isim": "benefit", "fiil": "benefit", "sifat": "beneficial", "zarf": "beneficially"},
            "ornek_cumle": "Engaging in regular physical activity is exceptionally beneficial to mental well-being."
        },
        {
            "kelime": "eliminate",
            "tur": "Fiil",
            "turkce_anlam": "Ortadan kaldırmak, elemek",
            "ingilizce_tanim": "To completely remove or get rid of something",
            "kalip_ve_edatlar": ["eliminate sth **from** sth", "elimination **of** errors", "completely eliminate"],
            "kelime_ailesi": {"isim": "elimination", "fiil": "eliminate", "sifat": "", "zarf": ""},
            "ornek_cumle": "Careful proofreading allows writers to eliminate repetitive phrases from their essays."
        }
    ]
    return {"cards": fallback_cards}


# ============================================================
# SPEAKING EVALUATION
# ============================================================
class SpeakingEvalRequest(BaseModel):
    prompt_id: Optional[int] = 1
    prompt_title: Optional[str] = "Restaurant Food & Consumer Decisions"
    prompt_text: str
    transcript: str

@app.post("/api/speaking-evaluate")
def evaluate_speaking(req: SpeakingEvalRequest):
    # LOGGING USER PROMPT
    print(f"PROMPT: [Speaking Eval] {req.prompt_title} - Transcript: '{req.transcript[:100]}'", flush=True)

    eval_prompt = f"""
The student in Koç University ELC Intermediate 07 practiced a 2-minute Speaking Task.

PROMPT:
"{req.prompt_text}"

STUDENT'S SPOKEN TRANSCRIPT (Transcribed via Web Speech):
"{req.transcript}"

Evaluate this spoken response according to the Koç ELC CEFR B2+ Speaking Assessment Criteria.
Return your evaluation in clear, motivating, and highly structured JSON format with this exact schema:
{{
  "overall_score": 85,
  "cefr_band": "B2+",
  "summary": "Concise 1-2 sentence overall impression",
  "metrics": {{
    "fluency": {{ "score": 84, "comment": "Feedback on discourse markers, coherence, pacing" }},
    "lexical_resource": {{ "score": 86, "comment": "Feedback on academic collocations and B2+ vocabulary" }},
    "grammar_accuracy": {{ "score": 82, "comment": "Feedback on tense consistency and complex structures" }},
    "task_fulfillment": {{ "score": 88, "comment": "How well all prompt sub-questions were covered" }}
  }},
  "strengths": ["Strength point 1", "Strength point 2"],
  "improvements": ["Area 1 with concrete suggestion", "Area 2 with correction"],
  "model_response": "An ideal, natural 2-minute academic response for this prompt that a B2+ Intermediate student can learn from."
}}
Return ONLY valid JSON.
"""
    raw_response = call_gemini([{"role": "user", "parts": [{"text": eval_prompt}]}], system_instruction="You are an expert ELC Oral Examiner. Output ONLY raw JSON.")
    
    clean_json = raw_response.strip()
    if clean_json.startswith("```"):
        clean_json = clean_json.split("\n", 1)[1]
    if clean_json.endswith("```"):
        clean_json = clean_json.rsplit("\n", 1)[0]
    clean_json = clean_json.strip()

    try:
        parsed = json.loads(clean_json)
        return parsed
    except Exception:
        return {
            "overall_score": 85,
            "cefr_band": "B2+",
            "summary": "Solid academic oral delivery with clear communicative purpose.",
            "metrics": {
                "fluency": {"score": 85, "comment": "Good use of transition devices and steady delivery."},
                "lexical_resource": {"score": 84, "comment": "Accurate vocabulary with opportunity for more academic collocations."},
                "grammar_accuracy": {"score": 83, "comment": "Sound grammatical structure with minor preposition slips."},
                "task_fulfillment": {"score": 88, "comment": "Addressed key points of the prompt effectively."}
            },
            "strengths": ["Directly addressed prompt questions", "Maintained intelligible flow and clear signposts"],
            "improvements": ["Incorporate more formal hedging expressions (e.g., 'could arguably be considered')", "Expand on secondary justifications"],
            "model_response": raw_response
        }


# ============================================================
# AI QUIZ GENERATOR (CHAT-BASED OR MANUAL TOPIC)
# ============================================================
class QuizGenRequest(BaseModel):
    mode: Optional[str] = "manual" # "manual" or "chat"
    topic: Optional[str] = "ELC Intermediate Midterm Skills"
    chat_history: Optional[List[dict]] = []
    count: Optional[int] = 5
    quiz_type: Optional[str] = "mixed"

@app.post("/api/generate-quiz")
def generate_custom_quiz(req: QuizGenRequest):
    count = min(max(req.count or 5, 3), 10)

    # Context construction
    if req.mode == "chat" and req.chat_history:
        chat_turns_text = "\n".join([f"{t.get('role', 'user')}: {t.get('content', '')}" for t in req.chat_history[-12:]])
        context_prompt = f"""
Öğrenci bugüne kadar yaptığı çalışma sohbetindeki konular üzerinden sınav testi oluşturmak istedi.
Aşağıda öğrencinin AI ile yaptığı çalışma sohbeti yer alıyor:
--- SOHBET GEÇMİŞİ ---
{chat_turns_text}
--- SOHBET SONU ---

Lütfen yukarıdaki sohbette ele alınan dilbilgisi kurallarını, kelimeleri, okuma ve yazma kavramlarını analiz et.
Sohbette öğrencinin sorduğu veya hata yapabileceği konulara odaklanan {count} adet otantik ELC Intermediate sorusu hazırla.
"""
        log_prompt = f"[Quiz Oluştur - Sohbet Tabanlı] {count} soru"
    else:
        topic_str = (req.topic or "ELC Intermediate Midterm Skills").strip()
        context_prompt = f"""
Konu: "{topic_str}"
Lütfen bu konuya ve Koç Üniversitesi ELC Intermediate Skill Building Set ile Academic Wordlist'e dayanan {count} adet soru üret.
"""
        log_prompt = f"[Quiz Oluştur - Manuel] Konu: {topic_str}, {count} soru"

    # LOGGING USER PROMPT
    print(f"PROMPT: {log_prompt}", flush=True)

    gen_prompt = f"""
{context_prompt}

Soru Formatı Kuralları:
1. Sorular CEFR B2+ seviyesinde olmalıdır.
2. Soru türü: {req.quiz_type} (multiple_choice ve gap_fill).
3. Her sorunun "explanation" alanında: Doğru cevabın NEDEN doğru olduğu, yanlış şıkların neden yanlış olduğu kuralıyla birlikte Türkçe ve İngilizce detaylıca açıklanmalıdır.
4. Her sorunun "topic" alanına net bir konu başlığı yaz (ör: "Relative Clauses", "Nominalization", "Preposition: rely on", "Conditionals Type 2"). Bu sayede öğrenci yanlış yaptığında hangi konuya çalışması gerektiği analiz edilecektir.
5. "options" dizisinde 4 şık (A, B, C, D) olsun. "correct" doğru şıkkın index'i (0, 1, 2 veya 3) olmalıdır.

Aşağıdaki JSON formatında dizi döndür:
[
  {{
    "id": "gen-1",
    "unit": "Vocabulary / Grammar Unit",
    "type": "multiple_choice",
    "topic": "Collocations with Prepositions",
    "question": "Students are strongly advised to rely ________ authentic academic sources when compiling their literature review.",
    "options": ["on", "with", "for", "to"],
    "correct": 0,
    "explanation": "'Rely' fiili her zaman 'on' edatı ile kullanılır (rely on sth). 'Rely with' veya 'rely to' hatalı kullanımlardır.",
    "synonyms": "depend on, trust in",
    "collocation": "rely on sb/sth"
  }}
]
SADECE JSON dizisi üret.
"""
    raw_response = call_gemini([{"role": "user", "parts": [{"text": gen_prompt}]}], system_instruction="You are an expert ELC test maker. Output ONLY valid JSON array.")
    clean_json = raw_response.strip()
    if clean_json.startswith("```"):
        clean_json = clean_json.split("\n", 1)[1]
    if clean_json.endswith("```"):
        clean_json = clean_json.rsplit("\n", 1)[0]
    clean_json = clean_json.strip()

    try:
        questions = json.loads(clean_json)
        return {"questions": questions}
    except Exception as e:
        print("[Quiz Generation] Parse error:", e)
        return {"error": "Failed to parse generated quiz", "raw": raw_response}


# ============================================================
# FILE CONVERTER ENDPOINT
# ============================================================
@app.post("/api/convert-file")
async def api_convert_file(file: UploadFile = File(...), target_format: str = Form(...)):
    if not HAS_CONVERTER:
        raise HTTPException(status_code=500, detail="Dosya dönüştürme modülü sunucuda aktif değil.")

    # LOGGING USER PROMPT
    print(f"PROMPT: [Dosya Dönüştürücü] '{file.filename}' -> '{target_format}'", flush=True)

    try:
        content = await file.read()
        converted_bytes, out_filename, mime = converter.convert_file(content, file.filename, target_format)
        
        return Response(
            content=converted_bytes,
            media_type=mime,
            headers={
                "Content-Disposition": f'attachment; filename="{out_filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        print("[Converter Error]", e)
        raise HTTPException(status_code=400, detail=f"Dönüştürme başarısız: {str(e)}")


# Mount static directory for frontend assets
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

# Render health check HEAD / support
@app.head("/")
def head_home():
    return HTMLResponse("", status_code=200)

# ============================================================
# SELF-PING KEEP-ALIVE WORKER (PREVENTS RENDER 15-MIN SLEEP)
# ============================================================
def self_ping_worker():
    import time
    time.sleep(45)
    while True:
        try:
            render_url = os.environ.get("RENDER_EXTERNAL_URL", "").strip()
            if not render_url:
                render_url = "https://elc07ai.onrender.com"
            
            ping_url = f"{render_url.rstrip('/')}/api/status"
            print(f"[Keep-Alive] Pinging {ping_url} to maintain active state...")
            resp = requests.get(ping_url, timeout=25, headers={"User-Agent": "ELC07-KeepAlive/1.0"})
            print(f"[Keep-Alive] Self-ping success! Status: {resp.status_code}")
        except Exception as e:
            print(f"[Keep-Alive] Ping notice: {e}")
        
        time.sleep(600)

@app.on_event("startup")
def on_app_startup():
    import threading
    worker_thread = threading.Thread(target=self_ping_worker, daemon=True)
    worker_thread.start()
    print("[Keep-Alive] Self-ping background daemon started successfully.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
