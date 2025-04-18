@echo off
echo Démarrage du monitoring automatique...
cd /d %~dp0src
python monitor.py
pause
