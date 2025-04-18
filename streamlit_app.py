#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# 1) Charger la config
load_dotenv(os.path.join(os.path.dirname(__file__), "config/.env"))

# 2) Configurer la page
st.set_page_config(
    page_title="🔍 Dashboard News Financière",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3) Titre & description
st.title("🔍 Agrégateur de News Financières")
st.markdown(
    """
    Ce dashboard affiche les derniers articles extraits, 
    leur sentiment et leur résumé (GPT ou fallback local).
    """
)

# 4) Charger les données
CSV_PATH = os.path.join("output", "rss_monitor.csv")
if not os.path.isfile(CSV_PATH):
    st.error(f"Le fichier de données est introuvable : `{CSV_PATH}`")
    st.stop()

df = pd.read_csv(CSV_PATH)
if df.empty:
    st.warning("Aucun article disponible pour le moment.")
    st.stop()

# 5) Sidebar – filtres
st.sidebar.header("Filtres")
# Filtrer par sentiment
sentiments = df["sentiment_label"].unique().tolist()
selected = st.sidebar.multiselect("Sentiments", sentiments, default=sentiments)
df = df[df["sentiment_label"].isin(selected)]

# Nombre d’articles affichés
st.sidebar.markdown(f"**Articles affichés :** {len(df)}")

# 6) Metrics en haut
col1, col2, col3 = st.columns(3)
col1.metric("Total extrait", len(pd.read_csv(os.path.join("output","rss_monitor.csv"))))
col2.metric("Filtrés affichés", len(df))
col3.metric("Sentiments uniques", len(sentiments))

# 7) Histogramme des sentiments
st.subheader("Répartition des sentiments")
sent_count = df["sentiment_label"].value_counts()
st.bar_chart(sent_count)

# 8) Affichage du tableau
st.subheader("Détail des articles")
# On s'assure que la colonne ai_summary existe
if "ai_summary" not in df.columns:
    df["ai_summary"] = ""
# Colonnes à montrer
cols = ["published", "title", "sentiment_label", "sentiment_score", "ai_summary"]
st.dataframe(
    df[cols].sort_values("published", ascending=False).reset_index(drop=True),
    use_container_width=True,
)

# 9) Bouton de téléchargement CSV
@st.cache_data
def to_csv(data: pd.DataFrame) -> bytes:
    return data.to_csv(index=False).encode("utf-8-sig")

csv_data = to_csv(df[cols])
st.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=csv_data,
    file_name="news_financieres.csv",
    mime="text/csv",
)

# 10) Pied de page
st.markdown("---")
st.markdown(
    f"<small>Généré le {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</small>",
    unsafe_allow_html=True
)
