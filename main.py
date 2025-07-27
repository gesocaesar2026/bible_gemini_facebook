import os
import requests

API_KEY = "AIzaSyDybAXRfYv832CWNwY7rrVt_YNfYmkHpz8"

def generate_bible_reflection():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

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
