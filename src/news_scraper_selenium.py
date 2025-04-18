#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de scraping pour l'agrégateur de nouvelles financières (version Selenium + BeautifulSoup).
Ce script charge la page Google News dynamiquement et extrait des articles en fonction d'une requête.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_google_news_selenium(query, num_results=10):
    """
    Scrape des articles d'actualité à partir de Google News en utilisant Selenium et BeautifulSoup.
    
    Args:
        query (str): La recherche à effectuer (ex: "finance", "marché boursier").
        num_results (int): Nombre maximal d'articles à récupérer.
    
    Returns:
        list: Une liste de dictionnaires contenant le titre, l'URL et le résumé de chaque article.
    """
    # Construire l'URL de recherche Google News
    url = f"https://news.google.com/search?q={query}"
    
    # Initialisation du driver Chrome en mode headless
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Charger la page et attendre pour le chargement complet via JavaScript
    driver.get(url)
    time.sleep(5)  # Ajuste ce délai si nécessaire
    
    # Récupérer le code HTML complet de la page
    html = driver.page_source
    driver.quit()
    
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Trouver tous les éléments <article>
    articles = soup.find_all("article")
    print(f"Trouvé {len(articles)} articles bruts sur la page.")
    
    results = []
    for article in articles[:num_results]:
        # Essayer d'extraire le titre depuis une balise <h3> ; sinon, tenter <h4>
        title_elem = article.find("h3")
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            title_elem = article.find("h4")
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                # Aucun titre trouvé, passer cet article
                continue
        
        # Extraire le lien ; généralement dans la première balise <a>
        link_elem = article.find("a", href=True)
        if link_elem:
            # Le lien est souvent relatif, donc on ajoute le domaine
            link = "https://news.google.com" + link_elem["href"]
        else:
            continue
        
        # Extraire un résumé (toute la section texte)
        summary = article.get_text(separator=" ", strip=True)
        
        results.append({
            "title": title,
            "url": link,
            "summary": summary
        })
    
    return results

if __name__ == "__main__":
    query = "finance"
    articles = scrape_google_news_selenium(query, num_results=10)
    print(f"Nombre d'articles extraits: {len(articles)}")
    for i, art in enumerate(articles, 1):
        print(f"\nArticle {i}:")
        print("Titre :", art["title"])
        print("URL   :", art["url"])
        print("Résumé:", art["summary"])
        print("-" * 50)
