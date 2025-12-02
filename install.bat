@echo off
cd /d "%~dp0"

echo.
echo  =============================================
echo   DiabetesHelp PRO - Instalacion
echo  =============================================
echo.

echo [1/2] Instalando dependencias...
pip install -r requirements.txt -q

echo.
echo [2/2] Verificando instalacion...
python -c "import gradio; import requests; print('OK')" 2>nul
if errorlevel 1 (
    echo ERROR: Fallo la instalacion
    pause
    exit /b 1
)

echo.
echo  =============================================
echo   Instalacion completada!
echo  =============================================
echo.
echo  Ahora configura tu API Key:
echo.
echo  1. Ve a https://openrouter.ai/
echo  2. Crea cuenta gratis ($5 de credito)
echo  3. Copia tu API Key
echo  4. Crea archivo .env con:
echo.
echo     OPENROUTER_API_KEY=sk-or-v1-tu-key
echo.
echo  Luego ejecuta: run.bat
echo.
pause
