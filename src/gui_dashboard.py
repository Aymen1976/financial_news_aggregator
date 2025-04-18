#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Config page ---
st.set_page_config(
    page_title="📈 Dashboard News Financières",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Agrégateur de News Financières")
st.markdown(
    "Analyse automatique d'articles économiques et financiers "
    "avec détection de sentiment et résumé GPT."
)

# --- Chargement des données ---
DATA_JSON = os.path.join("..", "output", "yahoo_finance.json")
if not os.path.exists(DATA_JSON):
    st.error(f"Fichier introuvable : `{DATA_JSON}`")
    st.stop()

try:
    df = pd.read_json(DATA_JSON)
except Exception as e:
    st.error(f"Impossible de lire `{DATA_JSON}` :\n\n{e}")
    st.stop()

# Convertir la date de publication en datetime
df["published"] = pd.to_datetime(df["published"], errors="coerce")

# --- Sidebar : filtres ---
st.sidebar.header("🔎 Filtres")
# Plage de dates
min_date, max_date = st.sidebar.date_input(
    "📅 Plage de publication",
    value=[df["published"].dt.date.min(), df["published"].dt.date.max()]
)
# Sentiments
all_sentiments = df["sentiment_label"].unique().tolist()
selected_sentiments = st.sidebar.multiselect(
    "🙂 Sentiments",
    options=all_sentiments,
    default=all_sentiments
)
# Mot‑clé dans le titre
keyword = st.sidebar.text_input("🔍 Mot‑clé dans le titre")

# Appliquer les filtres
mask = (
    df["published"].dt.date.between(min_date, max_date) &
    df["sentiment_label"].isin(selected_sentiments)
)
if keyword:
    mask &= df["title"].str.contains(keyword, case=False, na=False)

df_filtered = df[mask].copy()

# Si la colonne ai_summary n’existe pas (ancien CSV), on la crée vide
if "ai_summary" not in df_filtered.columns:
    df_filtered["ai_summary"] = "—"

# --- Affichage des articles ---
st.subheader("📰 Derniers articles")
columns_to_show = [
    "published", "title", "sentiment_label", "sentiment_score", "ai_summary"
]
st.dataframe(
    df_filtered[columns_to_show]
             .sort_values("published", ascending=False)
             .rename(columns={
                 "published": "Date",
                 "title": "Titre",
                 "sentiment_label": "Sentiment",
                 "sentiment_score": "Score",
                 "ai_summary": "Résumé GPT"
             }),
    use_container_width=True
)

# --- Distribution des sentiments ---
st.subheader("📈 Répartition des sentiments")
sent_counts = df_filtered["sentiment_label"].value_counts().reindex(all_sentiments, fill_value=0)
st.bar_chart(sent_counts)

# --- Footer ---
st.markdown("---")
st.markdown("© Projet Agrégateur — 🤖 ChatGPT & Streamlit")
