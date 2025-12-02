@echo off
cd /d "%~dp0"

echo.
echo  =============================================
echo   DiabetesHelp PRO
echo  =============================================
echo.
echo  Iniciando servidor...
echo  URL: http://localhost:7860
echo.

python src/app.py

if errorlevel 1 (
    echo.
    echo  ERROR: Fallo al iniciar
    echo  Verifica que tengas .env con tu API Key
    echo.
)

pause
