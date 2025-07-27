
import json
import os
import random
import requests
import google.generativeai as genai

# إعداد المفتاح
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
genai.configure(api_key=GEMINI_API_KEY)

# إعداد نموذج Gemini
model = genai.GenerativeModel("gemini-pro")

# إعداد فيسبوك
PAGE_ID = "90118319153"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"


# مسار ملف تخزين البوستات التي تم الرد عليها
REPLIED_FILE = "replied.json"

# تحميل البوستات التي تم الرد عليها
if os.path.exists(REPLIED_FILE):
    with open(REPLIED_FILE, "r", encoding="utf-8") as f:
        replied = json.load(f)
else:
    replied = []

# استدعاء أحدث المنشورات
def get_latest_posts():
    url = f"https://graph.facebook.com/{PAGE_ID}/posts"
    params = {
        "access_token": ACCESS_TOKEN,
        "limit": 5
    }
    res = requests.get(url, params=params)
    return res.json().get("data", [])

# توليد التأمل من Gemini
def get_bible_reflection():
    prompt = "أعطني آية عشوائية من الكتاب المقدس وتأمل مشجع باللغة العربية، ليتم نشرها على الفيسبوك. اجعل النص طويلًا وبأسلوب إنساني وقريب من القلب."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ خطأ من Gemini: {e}")
        return None

# نشر منشور على فيسبوك
def post_to_facebook(message):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "access_token": ACCESS_TOKEN,
        "message": message
    }
    res = requests.post(url, data=params)
    print(f"📤 Facebook Response: {res.status_code} {res.text}")
    return res.ok

# حفظ المنشورات التي تم الرد عليها
def save_replied():
    with open(REPLIED_FILE, "w", encoding="utf-8") as f:
        json.dump(replied, f, ensure_ascii=False, indent=2)

# ================================
# 📌 الخط الرئيسي
# ================================

# 1. جلب أحدث منشورات الصفحة
posts = get_latest_posts()

# 2. اختيار أول منشور لم يتم الرد عليه
target_post = None
for post in posts:
    if post["id"] not in replied:
        target_post = post
        break

if not target_post:
    print("✅ لا توجد منشورات جديدة للرد عليها.")
    exit()

print(f"🎯 جاري الرد على المنشور: {target_post['id']}")

# 3. توليد التأمل
reflection = get_bible_reflection()

if not reflection:
    print("❌ فشل في الحصول على تأمل من Gemini.")
    exit()

# 4. تكوين الرسالة النهائية
final_message = reflection + "\n\n🙏 الرب يباركك! شاركنا بأكثر آية تلمسك ❤️"

# 5. نشر على فيسبوك
success = post_to_facebook(final_message)

# 6. حفظ المنشور في قائمة "تم الرد عليه"
if success:
    replied.append(target_post["id"])
    save_replied()
    print("✅ تم الرد على المنشور وتحديث الملف.")
else:
    print("❌ فشل في النشر على فيسبوك.")
