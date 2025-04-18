#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
send_report.py

Envoie par e‑mail le rapport PDF quotidien généré par daily_report.py.
"""

import os
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

# 1) Charger les variables d’environnement
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
SMTP_SERVER   = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD= os.getenv("EMAIL_PASSWORD")
RECIPIENT     = os.getenv("REPORT_RECIPIENT")  # à ajouter dans .env

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT]):
    print("❌ Assurez‑vous que EMAIL_ADDRESS, EMAIL_PASSWORD et REPORT_RECIPIENT sont définis dans config/.env")
    sys.exit(1)

# 2) Construire le chemin du PDF du jour
today = datetime.now().strftime("%Y-%m-%d")
pdf_path = os.path.join(os.path.dirname(__file__), "..", "reports", f"report_{today}.pdf")
if not os.path.exists(pdf_path):
    print(f"❌ Le rapport n’existe pas : {pdf_path}")
    sys.exit(1)

# 3) Préparer le message
msg = EmailMessage()
msg["Subject"] = f"📒 Rapport Financier du {today}"
msg["From"]    = EMAIL_ADDRESS
msg["To"]      = RECIPIENT
msg.set_content(f"Bonjour,\n\nVous trouverez en pièce jointe le rapport financier du {today}.\n\nBonne journée.")

# 4) Joindre le PDF
with open(pdf_path, "rb") as f:
    data = f.read()
    msg.add_attachment(data, maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

# 5) Envoyer
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print(f"✅ Rapport envoyé à {RECIPIENT}")
except Exception as e:
    print(f"❌ Échec de l’envoi : {e}")
    sys.exit(1)
