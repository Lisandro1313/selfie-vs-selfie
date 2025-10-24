@echo off
echo ===============================================
echo     🚀 Preparar Selfie vs Selfie para Railway
echo ===============================================
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no instalado. Descarga desde: https://git-scm.com
    pause
    exit /b 1
)

echo ✅ Git instalado
echo.

REM Ejecutar test de pre-despliegue
echo 🧪 Ejecutando test de pre-despliegue...
.venv\Scripts\python.exe test_deployment.py
if errorlevel 1 (
    echo ❌ Test fallido. Revisar errores arriba.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo        🎉 ¡Listo para Railway!
echo ===============================================
echo.
echo 📋 Próximos pasos:
echo.
echo 1. Subir a GitHub:
echo    git init
echo    git add .
echo    git commit -m "🎮 Selfie vs Selfie Online"
echo    git remote add origin TU_REPO_URL
echo    git push -u origin main
echo.
echo 2. Ir a railway.app
echo 3. Deploy from GitHub repo
echo 4. Seleccionar tu repositorio
echo.
echo 🌐 Tu juego estará online en minutos!
echo 📖 Ver: DESPLIEGUE_RAPIDO.md
echo.
pause