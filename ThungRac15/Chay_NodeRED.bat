@echo off
echo ==========================================
echo   KHOI DONG NODE-RED (MIDDLEWARE TANG 3)
echo   Editor   : http://localhost:1880
echo   Dashboard: http://localhost:1880/ui
echo ==========================================
cd /d "%~dp0nodered"
node node_modules\node-red\red.js -u .
pause
