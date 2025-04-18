#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import hashlib
from news_scraper_rss import scrape_yahoo_finance_rss
from data_exporter import save_articles

# Pour éviter de republier les mêmes articles
def hash_article(article):
    """Crée un hash unique basé sur le titre + date"""
    key = f"{article['title']}{article['published']}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def main(pause_interval=60):
    print("📡 Démarrage de la surveillance continue...\n")
    seen_hashes = set()

    try:
        while True:
            articles = scrape_yahoo_finance_rss(num_results=10)
            new_articles = []

            for article in articles:
                article_hash = hash_article(article)
                if article_hash not in seen_hashes:
                    new_articles.append(article)
                    seen_hashes.add(article_hash)

            if new_articles:
                print(f"\n🆕 Nouveaux articles détectés : {len(new_articles)}")
                for art in new_articles:
                    print(f"- {art['title']} ({art['published']})")
                    print(f"  Sentiment : {art['sentiment_label']} ({art['sentiment_score']})")
                    print(f"  Lien : {art['url']}")
                    print("-" * 60)

                print("💾 Sauvegarde des nouveaux articles...")
                save_articles(new_articles, base_filename="rss_monitor")

                # Bip sonore (Windows uniquement)
                try:
                    import winsound
                    winsound.Beep(1000, 500)
                except:
                    pass
            else:
                print("⏳ Aucun nouvel article... Attente...")

            time.sleep(pause_interval)

    except KeyboardInterrupt:
        print("\n🛑 Surveillance interrompue par l'utilisateur.")

if __name__ == "__main__":
    main(pause_interval=60)  # Check every 60 seconds
