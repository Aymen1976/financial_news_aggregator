Agrégateur de Nouvelles Financières
==================================

Ce projet est un outil de scraping pour collecter des articles d'actualité financière depuis Google News.

Structure du projet :
----------------------
- config/.env: Fichier de configuration (par exemple, définir le terme de recherche via QUERY)
- data/: Dossier pour les logs ou autres données intermédiaires (peut rester vide)
- output/: Dossier où les résultats du scraping peuvent être enregistrés (pour une version future)
- src/news_scraper.py: Script de scraping principal
- run.bat: Script batch pour lancer automatiquement le scraper sans passer par le terminal
- requirements.txt: Liste des dépendances Python nécessaires
- readme.txt: Ce fichier d'instructions

Comment l'utiliser :
----------------------
1. Installez les dépendances :
   pip install -r requirements.txt

2. (Optionnel) Modifiez le fichier config/.env pour changer le terme de recherche (QUERY).

3. Lancez le script en exécutant run.bat ou via la commande :
   python src/news_scraper.py

Les résultats (titre, URL, résumé) seront affichés dans la console.

Bonne utilisation !
