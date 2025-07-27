import os
import requests
import json

# ⚙️ إعداد المتغيرات من البيئة
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
PAGE_ID = "90118319153"

# ✅ دالة توليد آية وتأمل من Gemini
def generate_devotion():
    print("🎯 جاري توليد آية وتأمل من Gemini...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = (
        "اكتبلي آية من الكتاب المقدس مناسبة لأي شخص بيمر بظروف صعبة، "
        "وتحتها تأمل  باللهجة المصرية، يكون كأن المسيح هو اللي بيكلم الشخص وبيطبطب عليه، "
        "خلي التأمل مشجع ويلمس القلب، لا تضف مقدمات ولا عناوين، فقط الآية والتأمل في سطرين أو ثلاثة."
    )

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        try:
            content = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            print("✅ تم توليد التأمل بنجاح.")
            return content
        except Exception as e:
            print("❌ خطأ أثناء تحليل رد Gemini:", e)
    else:
        print(f"❌ خطأ من Gemini: {response.status_code} - {response.text}")
    
    return None

# ✅ دالة النشر على صفحة فيسبوك
def post_to_facebook(message):
    print("📤 جاري النشر على فيسبوك...")

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم النشر على الصفحة بنجاح.")
    else:
        print(f"❌ فشل النشر على فيسبوك: {response.status_code} - {response.text}")

# ✅ تنفيذ الخطوات
if __name__ == "__main__":
    message = generate_devotion()
    if message:
        post_to_facebook(message)
    else:
        print("❌ لم يتم توليد رسالة.")
