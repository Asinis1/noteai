from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_note(content: str) -> dict:
    prompt = f"""Aşağıdaki not metnini analiz et ve SADECE JSON formatında yanıt ver. Markdown kullanma.

Not metni:
\"\"\"{content}\"\"\"

Şu formatta JSON döndür:
{{
  "summary": "Notun 2-3 cümlelik Türkçe özeti",
  "suggested_tags": ["etiket1", "etiket2", "etiket3"],
  "keywords": ["anahtar1", "anahtar2", "anahtar3", "anahtar4", "anahtar5"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    response_text = response.choices[0].message.content.strip()

    if "```" in response_text:
        lines = response_text.split("\n")
        cleaned = [l for l in lines if not l.startswith("```")]
        response_text = "\n".join(cleaned).strip()

    result = json.loads(response_text)
    return result