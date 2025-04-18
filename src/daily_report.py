#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
daily_report.py

Génère chaque matin un rapport PDF listant les derniers articles,
avec leur sentiment et résumé GPT/local.
"""

import os
import sys
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv

# Charger .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# Chemins
CSV_PATH   = os.path.join(os.path.dirname(__file__), "../output/rss_monitor.csv")
PDF_FOLDER = os.path.join(os.path.dirname(__file__), "../reports")
os.makedirs(PDF_FOLDER, exist_ok=True)

if not os.path.exists(CSV_PATH):
    print(f"❌ Fichier introuvable : {CSV_PATH}")
    sys.exit(1)

# Lire les données
df = pd.read_csv(CSV_PATH)
if df.empty:
    print("⚠️ Aucun article à inclure dans le rapport.")
    sys.exit(0)

# Fonction de nettoyage pour FPDF Latin‑1
def sanitize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # remplacer les apostrophes typographiques, etc.
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    # encoder en latin-1 en remplaçant les caractères impossibles
    return text.encode("latin-1", "replace").decode("latin-1")

# Préparer le PDF
today_str = datetime.now().strftime("%Y-%m-%d")
pdf_path = os.path.join(PDF_FOLDER, f"report_{today_str}.pdf")

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# En‑tête
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, sanitize(f"Rapport Financier du {today_str}"), ln=True, align="C")
pdf.ln(5)

# Tri et sélection
df = df.sort_values("published", ascending=False).head(20)

# Boucle sur les articles
pdf.set_font("Arial", "", 11)
for i, (_, row) in enumerate(df.iterrows(), 1):
    title     = sanitize(row.get("title", "Titre non disponible"))
    published = row.get("published", "")
    try:
        published = datetime.fromisoformat(published).strftime("%Y-%m-%d %H:%M")
    except Exception:
        published = sanitize(published)
    sentiment = sanitize(row.get("sentiment_label", ""))
    score     = row.get("sentiment_score", "")
    summary   = sanitize(row.get("ai_summary", ""))

    # Titre
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 6, f"{i}. {title}")
    # Métadonnées
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 5, f"   Date : {published}   |   Sentiment : {sentiment} ({score})")
    # Résumé
    if summary:
        pdf.multi_cell(0, 5, f"   Résumé : {summary}")
    pdf.ln(3)

# Pied de page
pdf.set_y(-15)
pdf.set_font("Arial", "I", 8)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
pdf.cell(0, 10, sanitize(f"Généré automatiquement le {timestamp}"), 0, 0, "C")

# Sauvegarde
pdf.output(pdf_path)
print(f"✅ Rapport PDF généré : {pdf_path}")
