#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
from sentiment_analyzer import analyze_sentiment
from smart_summarizer import summarize_article  # 🧠 GPT résumé

RSS_URL = "https://finance.yahoo.com/news/rss"

def scrape_yahoo_finance_rss(num_results=10):
    feed = feedparser.parse(RSS_URL)
    articles = []
    
    for entry in feed.entries[:num_results]:
        summary_text = entry.get("summary", entry.get("title", ""))
        ai_summary = summarize_article(summary_text)
        sentiment = analyze_sentiment(summary_text)

        articles.append({
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", "").strip(),
            "summary": summary_text.strip(),
            "published": entry.get("published", "").strip(),
            "sentiment_label": sentiment["label"],
            "sentiment_score": sentiment["polarity"],
            "ai_summary": ai_summary.strip() if isinstance(ai_summary, str) else ""
        })
    
    return articles

if __name__ == "__main__":
    from data_exporter import export_json, export_csv, export_excel

    results = scrape_yahoo_finance_rss(num_results=10)
    print(f"Articles extraits et analysés : {len(results)}")

    base = "yahoo_finance"
    path_json = export_json(results, base)
    path_csv = export_csv(results, base)
    path_excel = export_excel(results, base)

    print("\n📁 Fichiers exportés :")
    print("- JSON   :", path_json)
    print("- CSV    :", path_csv)
    print("- Excel  :", path_excel)
