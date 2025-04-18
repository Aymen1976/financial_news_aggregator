# smart_summarizer.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_article(text: str, max_tokens=150) -> str:
    if not openai.api_key:
        return "⚠️ Clé OpenAI manquante"

    if not text or len(text.strip()) == 0:
        return "⛔️ Aucun contenu à résumer"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Tu peux utiliser GPT-4 si tu y as accès
            messages=[
                {"role": "system", "content": "Tu es un assistant spécialisé dans la finance."},
                {"role": "user", "content": f"Résume l'article suivant en français de façon claire et concise :\n{text}"}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Erreur lors du résumé : {e}"
