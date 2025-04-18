#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de scraping simple pour l'agrégateur de nouvelles financières (Yahoo Finance).
Il récupère les derniers articles depuis finance.yahoo.com/news.
"""

import requests
from bs4 import BeautifulSoup

def scrape_yahoo_finance_news(num_results=10):
    url = "https://finance.yahoo.com/news"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erreur HTTP :", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    # Les articles sont dans des <li> avec la classe js-stream-content Pos(r)
    for item in soup.find_all("li", class_="js-stream-content Pos(r)")[:num_results]:
        # Le titre est dans un <h3>
        h3 = item.find("h3")
        if not h3:
            continue

        # Le lien est dans l'<a> à l'intérieur du h3
        a_tag = h3.find("a", href=True)
        if not a_tag:
            continue

        title = h3.get_text(strip=True)
        href = a_tag["href"]
        # Construire l'URL complète si nécessaire
        url_article = href if href.startswith("http") else f"https://finance.yahoo.com{href}"
        summary = item.get_text(separator=" ", strip=True)

        articles.append({
            "title": title,
            "url": url_article,
            "summary": summary
        })

    return articles

if __name__ == "__main__":
    results = scrape_yahoo_finance_news(num_results=10)
    print(f"Articles extraits : {len(results)}\n")
    for idx, art in enumerate(results, 1):
        print(f"{idx}. {art['title']}")
        print("URL   :", art["url"])
        print("Résumé:", art["summary"])
        print("-" * 60)
