#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
smart_summarizer.py

Essayez d’abord de résumer via l’API OpenAI. 
Si votre quota est dépassé, on bascule sur un résumé local grâce à Gensim.
"""

import os
import sys
import time
from dotenv import load_dotenv

# attempt local summarization
try:
    from gensim.summarization import summarize as local_summarize
except ImportError:
    local_summarize = None

# OpenAI v1.0+ client
try:
    from openai import OpenAI
except ImportError:
    print("❌ Erreur : installez openai>=1.0.0 (`pip install openai`).")
    sys.exit(1)

# Charger la config
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("❌ OPENAI_API_KEY manquante dans config/.env")
    sys.exit(1)

# Init client
client = OpenAI(api_key=API_KEY)

def summarize_article(text: str) -> str:
    """
    Résume `text`. 
    1) Essai GPT-3.5-turbo via l’API OpenAI.
    2) Si quota dépassé ou autre erreur, fallback local via Gensim.
    """
    # 1) Tentative via OpenAI
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                    "Tu es un assistant expert en finance, fournis un résumé clair et concis de l'article suivant."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        err = str(e)
        if "insufficient_quota" in err or "429" in err:
            print("⚠️ Quota OpenAI dépassé, utilisation du résumé local.")
        else:
            print(f"⚠️ Échec OpenAI ({e}), bascule résumé local.")
        # 2) Fallback local
        if local_summarize:
            try:
                # Gensim peut échouer si le texte est trop court
                summary = local_summarize(text, word_count=50)
                return summary or "Résumé local indisponible (texte trop court)."
            except Exception as le:
                print(f"⚠️ Erreur résumé local : {le}")
                return "Résumé indisponible"
        else:
            return "Résumé indisponible"

if __name__ == "__main__":
    sample = (
        "Le marché boursier américain a terminé en légère hausse aujourd'hui, "
        "porté par les technologiques après des commentaires rassurants de la Fed."
    )
    print("🔎 Texte original :", sample, "\n")
    print("📝 Résumé GPT/local :", summarize_article(sample))
