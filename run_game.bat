@echo off
echo ===============================================
echo        🎮 Selfie vs Selfie Online
echo ===============================================
echo.
echo 🌊 Juego multijugador con estética de Playa del Carmen
echo 📸 Reconocimiento de gestos con cámara web
echo.

REM Verificar que el entorno virtual existe
if not exist ".venv" (
    echo ❌ Entorno virtual no encontrado
    echo    Ejecuta install.bat primero
    pause
    exit /b 1
)

echo 🚀 Iniciando servidor de juego...
echo.
echo 🌐 El juego estará disponible en:
echo    http://localhost:5000
echo.
echo ⌨️  Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar el servidor
.venv\Scripts\python.exe rps_online\run_server.py

echo.
echo 👋 Servidor detenido
pause