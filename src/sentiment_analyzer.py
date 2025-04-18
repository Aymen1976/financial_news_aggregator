#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'analyse de sentiment basé sur TextBlob.
"""

from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """
    Analyse le sentiment d'un texte.
    
    Args:
        text (str): Le texte à analyser.
    
    Returns:
        dict: {
            "polarity": float,  # entre -1 (très négatif) et +1 (très positif)
            "subjectivity": float,  # entre 0 (objectif) et 1 (subjectif)
            "label": str  # "positif", "neutre" ou "négatif"
        }
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        label = "positif"
    elif polarity < -0.1:
        label = "négatif"
    else:
        label = "neutre"
    
    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "label": label
    }
