# 🚀 GUÍA RÁPIDA: Desplegar en Railway

## ✅ Pre-requisitos Completados
- ✅ Todas las dependencias instaladas
- ✅ Archivos de configuración listos
- ✅ App funciona localmente
- ✅ Test de pre-despliegue pasado

## 🌐 Pasos para Railway

### 1. Subir a GitHub
```bash
# Si no tienes Git inicializado
git init
git add .
git commit -m "🎮 Selfie vs Selfie - Listo para despliegue"

# Crear repositorio en GitHub y luego:
git remote add origin https://github.com/TU-USUARIO/selfie-vs-selfie.git
git push -u origin main
```

### 2. Desplegar en Railway
1. **Ve a** [railway.app](https://railway.app)
2. **Sign up** con GitHub
3. **"Deploy from GitHub repo"**
4. **Selecciona** tu repositorio `selfie-vs-selfie`
5. **Railway automáticamente:**
   - Detecta Python
   - Instala dependencias
   - Ejecuta `python server.py`
   - Asigna dominio

### 3. ¡Listo! 🎉
- **URL:** Railway te dará una URL como `https://selfie-vs-selfie-production.up.railway.app`
- **HTTPS:** Automático
- **SSL:** Incluido
- **Global:** Accesible desde cualquier lugar

## 🎮 Tu Juego Online

Una vez desplegado, cualquiera puede:
- **Abrir tu URL** desde cualquier dispositivo
- **Crear salas privadas** para jugar con amigos
- **Jugar contra IA** inmediatamente
- **Usar cámara web** para gestos
- **Competir en tiempo real**

## 📱 Compartir

```
🎮 ¡Juega Selfie vs Selfie Online!
🌐 https://tu-url.railway.app
📸 Piedra, papel o tijera con cámara
🤖 Modo IA disponible
🏆 Multijugador en tiempo real
🏖️ Estética Playa del Carmen
```

## 🔧 Variables de Entorno (Opcional)

En Railway > Settings > Variables:
```
SECRET_KEY=tu_clave_super_secreta_123
DEBUG=False
```

## 💰 Costos
- **Railway:** Gratis hasta 512MB RAM + $5/mes Pro
- **Heroku:** Gratis limitado + $7/mes Hobby
- **Render:** Gratis limitado + $7/mes

## 🆘 Si hay problemas
1. **Revisar logs** en Railway dashboard
2. **Verificar** que todos los archivos estén en GitHub
3. **Contactar** si necesitas ayuda

¡Tu juego estará online en 5 minutos! 🌍