import os
import requests

# إعدادات البيئة
ACCESS_TOKEN ="EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
PAGE_ID = "90118319153"
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"

def get_bible_message():
    prompt = """
    أعطني آية عشوائية من الكتاب المقدس، وتأمل طويل باللغة العربية بأسلوب مشجع ومليء بالرجاء، كأن السيد المسيح يتحدث مباشرة إلى القارئ ويشجّعه بكلمات مملوءة حبًا ورحمة.

    صيغة الرد يجب أن تكون هكذا:

    الآية: ...
    المرجع: ...
    التأمل: ...
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    try:
        # نحلل الاستجابة كنص عادي
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # استخراج البيانات يدويًا
        verse = ""
        reference = ""
        reflection = ""

        for line in text.splitlines():
            if line.startswith("الآية:"):
                verse = line.replace("الآية:", "").strip()
            elif line.startswith("المرجع:"):
                reference = line.replace("المرجع:", "").strip()
            elif line.startswith("التأمل:"):
                reflection = line.replace("التأمل:", "").strip()

        final_message = f"📖 {verse} ({reference})\n\n✝️ {reflection}"
        return final_message

    except Exception as e:
        print("❌ خطأ أثناء تحليل رد Gemini:", e)
        return "حدث خطأ أثناء توليد التأمل. 🙏"

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=params)
    print("✅ Facebook response:", response.status_code, response.text)

if __name__ == "__main__":
    msg = get_bible_message()
    print("📝 Generated Message:\n", msg)
    post_to_facebook(msg)
