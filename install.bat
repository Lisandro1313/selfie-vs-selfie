@echo off
echo ===============================================
echo      🎮 Selfie vs Selfie - Instalacion 
echo ===============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8+ primero.
    echo    Descargalo desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Crear entorno virtual si no existe
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual existente encontrado
)

echo.

REM Activar entorno virtual e instalar dependencias
echo 📥 Instalando dependencias...
.venv\Scripts\pip install -r rps_online\requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

echo ===============================================
echo          🚀 Instalacion Completa! 
echo ===============================================
echo.
echo Para ejecutar el juego:
echo   1. Ejecuta: run_game.bat
echo   2. Abre tu navegador en: http://localhost:5000
echo.
echo ¡Disfruta jugando Selfie vs Selfie! 🎯
echo.
pause