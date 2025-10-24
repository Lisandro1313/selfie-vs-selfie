#!/usr/bin/env python3
"""
Test de pre-despliegue para Selfie vs Selfie
Verifica que todo esté listo para producción
"""

import sys
import os

def test_imports():
    """Probar que todas las dependencias se pueden importar"""
    print("🧪 Testeando imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError:
        print("❌ Flask no instalado")
        return False
    
    try:
        import flask_socketio
        print(f"✅ Flask-SocketIO importado")
    except ImportError:
        print("❌ Flask-SocketIO no instalado")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV no instalado")
        return False
    
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe {mp.__version__}")
    except ImportError:
        print("❌ MediaPipe no instalado")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError:
        print("❌ NumPy no instalado")
        return False
    
    return True

def test_files():
    """Verificar que los archivos necesarios existen"""
    print("\n📁 Verificando archivos...")
    
    required_files = [
        'Procfile',
        'requirements.txt',
        'runtime.txt',
        'server.py',
        'rps_online/app.py',
        'rps_online/gesture_detector.py',
        'rps_online/templates/index.html',
        'rps_online/templates/game.html',
        'rps_online/static/js/game.js'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - FALTANTE")
            all_exist = False
    
    return all_exist

def test_app_startup():
    """Probar que la app puede iniciar"""
    print("\n🚀 Testeando startup de la app...")
    
    try:
        sys.path.append('rps_online')
        from rps_online.app import app, socketio
        print("✅ App importada correctamente")
        
        # Test básico de configuración
        if app.config.get('SECRET_KEY'):
            print("✅ SECRET_KEY configurada")
        else:
            print("⚠️ SECRET_KEY no configurada (usar variable de entorno)")
        
        return True
    except Exception as e:
        print(f"❌ Error al importar app: {e}")
        return False

def main():
    print("🎮 Selfie vs Selfie - Test de Pre-Despliegue")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Archivos", test_files),
        ("App Startup", test_app_startup)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        result = test_func()
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ¡LISTO PARA DESPLIEGUE!")
        print("🚀 Puedes subir a Railway/Heroku/Render")
        print("📖 Ver: DEPLOYMENT_RAILWAY.md")
    else:
        print("❌ HAY PROBLEMAS - Revisar errores arriba")
        print("🔧 Instalar dependencias: pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())