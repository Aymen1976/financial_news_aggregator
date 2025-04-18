#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from news_scraper_rss import scrape_yahoo_finance_rss

# Charger le fichier .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body, to_email):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise Exception("⚠️ EMAIL_ADDRESS ou EMAIL_PASSWORD manquant dans le fichier .env")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email envoyé avec succès.")
    except Exception as e:
        print("❌ Erreur lors de l'envoi de l'email :", e)

if __name__ == "__main__":
    print("📨 Envoi du dernier article par email...")

    articles = scrape_yahoo_finance_rss(num_results=1)
    if not articles:
        print("❌ Aucun article trouvé.")
        exit()

    article = articles[0]
    subject = f"📰 {article['title']}"
    content = f"""Titre : {article['title']}
Date : {article['published']}
Sentiment : {article['sentiment_label']} ({article['sentiment_score']})
Résumé :
{article['summary']}

🔗 Lien : {article['url']}
"""

    # Remplace l'adresse ici par ton adresse de réception
    send_email(subject, content, "benchoamino@gmail.com")
