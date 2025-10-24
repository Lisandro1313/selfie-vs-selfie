#!/usr/bin/env python3
"""
Servidor de producción para Selfie vs Selfie Online
Optimizado para Railway y otros servicios de hosting
"""

import os
import sys
from rps_online.app import app, socketio

def main():
    """Función principal para producción"""
    print("🚀 Iniciando Selfie vs Selfie Online - Producción")
    print("🌊 Juego multijugador con estética de Playa del Carmen")
    
    # Configuración para producción
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Servidor en puerto: {port}")
    print(f"🔧 Debug mode: {debug}")
    print("📱 Funcionalidades:")
    print("   ✅ Multijugador en tiempo real")
    print("   🤖 Modo contra IA")
    print("   📸 Reconocimiento de gestos")
    print("   🏆 Sistema de puntuación")
    print("   📱 Responsive design")
    print("-" * 50)
    
    try:
        # Ejecutar servidor con configuración de producción
        socketio.run(
            app, 
            host=host, 
            port=port, 
            debug=debug,
            allow_unsafe_werkzeug=True,
            use_reloader=False,  # Desactivar en producción
            log_output=True
        )
    except Exception as e:
        print(f"❌ Error al ejecutar el servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()