import os
import requests

# ====== إعداد المتغيرات ======
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
PAGE_ID = "90118319153"

# ====== توليد رسالة من Gemini ======
def get_gemini_devotional():
    print("🎯 جاري توليد آية وتأمل من Gemini...")

    prompt = (
        "اكتبلي آية من الكتاب المقدس مناسبة لأي شخص بيمر بظروف صعبة، "
        "وتحتها تأمل قصير باللهجة المصرية، يكون كأن المسيح هو اللي بيكلم الشخص وبيطبطب عليه، "
        "خلي التأمل قصير ومشجع ويلمس القلب، لا تضف مقدمات ولا عناوين، فقط الآية والتأمل في سطرين أو ثلاثة."
    )

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    params = {"key": GEMINI_API_KEY}

    response = requests.post(url, headers=headers, params=params, json=payload)

    if response.status_code == 200:
        result = response.json()
        message = result["candidates"][0]["content"]["parts"][0]["text"]
        return message.strip()
    else:
        print(f"❌ خطأ من Gemini: {response.status_code} - {response.text}")
        return None

# ====== نشر الرسالة على فيسبوك ======
def post_to_facebook(message):
    print("🚀 جاري النشر على فيسبوك...")

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("✅ تم النشر على فيسبوك بنجاح!")
        return True
    else:
        print(f"❌ فشل النشر على فيسبوك: {response.status_code} - {response.text}")
        return False

# ====== تنفيذ الخطوات ======
if __name__ == "__main__":
    if not all([GEMINI_API_KEY, ACCESS_TOKEN, PAGE_ID]):
        print("❌ تأكد من ضبط متغيرات البيئة: GEMINI_API_KEY, ACCESS_TOKEN, PAGE_ID")
        exit(1)

    message = get_gemini_devotional()
    if message:
        post_to_facebook(message)
    else:
        print("❌ لم يتم توليد رسالة.")
