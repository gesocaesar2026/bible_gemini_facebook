import os
import requests
from datetime import datetime

# ---------- 1. إعداد المفاتيح ----------
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"

PAGE_ID ="90118319153"

# ---------- 2. توليد آية وتأمل من جيميناي ----------
def generate_bible_reflection():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    prompt = (
        "اكتبلي آية من الكتاب المقدس مناسبة لأي شخص بيمر بظروف صعبة، "
        "وتحتها تأمل قصير باللهجة المصرية، يكون كأن المسيح هو اللي بيكلم الشخص وبيطبطب عليه، "
        "خلي التأمل قصير ومشجع ويلمس القلب، لا تضف مقدمات ولا عناوين، فقط الآية والتأمل في سطرين أو ثلاثة."
    )

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"❌ خطأ من Gemini: {response.status_code} - {response.text}")
        return None

# ---------- 3. نشر المنشور على فيسبوك ----------
def post_to_facebook(message):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        post_id = response.json().get("id")
        print(f"✅ تم نشر الرسالة بنجاح على فيسبوك. ID: {post_id}")
    else:
        print(f"❌ خطأ أثناء النشر على فيسبوك: {response.status_code} - {response.text}")

# ---------- 4. التشغيل التلقائي ----------
def main():
    print(f"🎯 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] جاري توليد آية وتأمل من Gemini...")
    message = generate_bible_reflection()

    if message:
        print("✅ تم التوليد بنجاح. جاري النشر على فيسبوك...")
        post_to_facebook(message)
    else:
        print("❌ لم يتم توليد رسالة. لم يتم النشر.")

if __name__ == "__main__":
    main()
