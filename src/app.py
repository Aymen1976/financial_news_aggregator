# src/app.py

import news_scraper_rss
import data_exporter

def main():
    print("📡 Lancement de l'agrégateur de news financières...\n")

    # Étape 1 : Récupérer les articles via RSS
    articles = news_scraper_rss.get_financial_news()
    print(f"\nArticles récupérés : {len(articles)}")

    # Étape 2 : Exporter les articles
    if articles:
        data_exporter.save_articles(articles, base_filename="yahoo_finance")
        print("✅ Export terminé avec succès.")
    else:
        print("⚠️ Aucun article à exporter.")

if __name__ == "__main__":
    main()
