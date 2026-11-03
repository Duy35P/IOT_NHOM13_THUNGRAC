@echo off
chcp 65001 >nul
title SERVER DATABASE MIDDLEWARE IOT (MYSQL LARAGON) - NHOM 15
echo ====================================================================
echo   HE THONG TRUYEN THONG & LUU TRU DATABASE IOT - NHOM 15
echo   Database: MySQL Laragon (127.0.0.1:3306 / Database: thung_rac_db)
echo   Broker  : broker.hivemq.com:1883
echo ====================================================================
echo.
echo [*] Luu y: Hay dam bao Laragon da duoc bat (bam "Start All" tren Laragon).
echo.
cd /d "%~dp0"
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python -u middleware.py
pause
