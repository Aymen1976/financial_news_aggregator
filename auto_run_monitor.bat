@echo off
REM ================================================
REM  Lancement automatique du monitor en local
REM ================================================
cd /d %~dp0\src
python monitor.py
