#!/usr/bin/env python3
"""
Servidor principal para Selfie vs Selfie Online
Script optimizado para desarrollo y producción
"""

import os
import sys
from app import app, socketio

def main():
    """Función principal para ejecutar el servidor"""
    print("🎮 Iniciando Selfie vs Selfie Online...")
    print("📱 Juego multijugador de Piedra, Papel o Tijera")
    print("🌊 Estética inspirada en Playa del Carmen")
    print("-" * 50)
    
    # Configuración del servidor
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Servidor ejecutándose en:")
    print(f"   Local: http://127.0.0.1:{port}")
    print(f"   Red:   http://{get_local_ip()}:{port}")
    print("-" * 50)
    print("📝 Funcionalidades disponibles:")
    print("   ✅ Multijugador en tiempo real")
    print("   🤖 Modo contra IA")
    print("   📸 Reconocimiento de gestos")
    print("   🏆 Sistema de puntuación")
    print("   📱 Responsive design")
    print("-" * 50)
    print("⌨️  Presiona Ctrl+C para detener el servidor")
    print()
    
    try:
        # Ejecutar servidor con SocketIO
        socketio.run(
            app, 
            host=host, 
            port=port, 
            debug=debug,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error al ejecutar el servidor: {e}")
        sys.exit(1)

def get_local_ip():
    """Obtiene la IP local de la máquina"""
    import socket
    try:
        # Crear socket temporal para obtener IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == '__main__':
    main()