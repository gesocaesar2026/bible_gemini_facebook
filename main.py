import os
import requests
import json

# مفاتيح API
GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
ACCESS_TOKEN = "EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
PAGE_ID = "90118319153"

def generate_message():
    print("🎯 جاري توليد رسالة مؤثرة من الرب يسوع بواسطة Gemini...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = """
    من فضلك اكتب رسالة مؤثرة وكأنها من الرب يسوع إلى القارئ، بأسلوب حنون ومشجع ولمس للمشاعر.
    اجعلها شخصية تبدأ بنداء مثل "يا ابني" أو "يا ابنتي" وتكلم كأن المسيح يخاطب شخصًا مجروحًا ويشجعه.
    لا تضع آيات، فقط اجعلها رسالة مشجعة، لا تزيد عن 500 حرف، باللهجة المصرية الخفيفة المقبولة روحيًا.
    """

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            print("✅ تم توليد الرسالة بنجاح.")
            return content.strip()
        except Exception as e:
            print("❌ فشل في قراءة رد Gemini:", e)
    else:
        print(f"❌ خطأ من Gemini: {response.status_code} - {response.text}")
    return None

def post_to_facebook(message):
    print("📤 جاري النشر على فيسبوك...")
    post_url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(post_url, data=params)
    if response.status_code == 200:
        print("✅ تم النشر بنجاح على فيسبوك.")
    else:
        print(f"❌ فشل النشر على فيسبوك: {response.status_code} - {response.text}")

def main():
    message = generate_message()
    if message:
        print("\n📩 الرسالة التي تم توليدها:\n")
        print(message)
        print("\n----------------------------------------\n")
        post_to_facebook(message)
    else:
        print("🚫 لم يتم توليد أو نشر الرسالة.")

if __name__ == "__main__":
    main()
