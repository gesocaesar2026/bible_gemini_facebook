import requests
import os

GEMINI_API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"
ACCESS_TOKEN ="EAAUmqjbT57QBOZBdPSIvCfyGmfSEyFx2tWLlLNaMZAO9ZBKCd4EJEFhtbgZBm87N6KNYqvl5QGlLurkgHLjVNFUPU9MVJXtfQbGlz45hJX79Wd3PwEp7OF50THiZAqG0A0M3DNF290CdPeYIEMG5YB99uFg3UKK04iqDZBRZCkYWMbE7ltZCHl4ZAEjMSWHi1NeYIgEcs25WIdo7kIRwqWdgZD"
PAGE_ID = "90118319153"

def get_devotional_from_gemini():
    prompt = (
        "اكتبلي آية من الكتاب المقدس مناسبة لأي شخص بيمر بظروف صعبة، "
        "وتحتها تأمل قصير باللهجة المصرية، يكون كأن المسيح هو اللي بيكلم الشخص وبيطبطب عليه، "
        "خلي التأمل قصير ومشجع ويلمس القلب، لا تضف مقدمات ولا عناوين، فقط الآية والتأمل في سطرين أو ثلاثة."
    )

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )

    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            print("❌ فشل في تحليل رد Gemini.")
            return None
    else:
        print(f"❌ خطأ من Gemini: {response.status_code} - {response.text}")
        return None

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        print("✅ تم نشر التأمل بنجاح على فيسبوك.")
    else:
        print(f"❌ فشل في النشر على فيسبوك: {response.status_code} - {response.text}")

def main():
    print("🎯 جاري توليد آية وتأمل من Gemini...")
    message = get_devotional_from_gemini()
    if message:
        print("📝 التأمل الذي تم توليده:\n", message)
        post_to_facebook(message)
    else:
        print("❌ لم يتم توليد رسالة.")

if __name__ == "__main__":
    main()
