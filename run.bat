@echo off
cd /d %~dp0
echo ===============================
echo  Lancement de l'Agrégateur de Nouvelles Financières
echo ===============================
python src/news_scraper.py
pause
