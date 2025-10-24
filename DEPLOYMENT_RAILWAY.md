# 🚀 Despliegue de Selfie vs Selfie Online

## 🌐 Railway (Recomendado)

### Paso 1: Preparar Railway

1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta gratuita
3. Conecta tu GitHub

### Paso 2: Desplegar desde GitHub

1. **Fork o sube** este repositorio a tu GitHub
2. En Railway: **"New Project" → "Deploy from GitHub repo"**
3. Selecciona el repositorio `selfie-vs-selfie`
4. Railway detectará automáticamente Python y usará el `Procfile`

### Paso 3: Variables de Entorno (Opcional)

```env
DEBUG=False
SECRET_KEY=tu_clave_secreta_produccion
```

### Paso 4: ¡Listo!

- Railway generará una URL como: `https://tu-proyecto.railway.app`
- El juego estará disponible globalmente 🌍

## 🌐 Alternativas de Hosting

### Heroku

```bash
# Instalar Heroku CLI
heroku create selfie-vs-selfie-tu-nombre
git push heroku main
```

### Render

1. Conecta GitHub en [render.com](https://render.com)
2. Selecciona repositorio
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python server.py`

### DigitalOcean App Platform

1. Conecta GitHub
2. Detecta automáticamente Python
3. Usa configuración por defecto

## 📋 Checklist Pre-Despliegue

- ✅ `Procfile` configurado
- ✅ `requirements.txt` optimizado
- ✅ `runtime.txt` especificado
- ✅ `server.py` para producción
- ✅ Variables de entorno configuradas
- ✅ OpenCV headless para servidores

## 🔧 Configuración de Producción

### Archivos Clave

- `server.py` - Servidor optimizado
- `Procfile` - Comando de inicio
- `requirements.txt` - Dependencias
- `railway.json` - Configuración Railway

### Variables de Entorno

```env
PORT=5000              # Puerto (automático en Railway)
HOST=0.0.0.0           # Host (automático)
DEBUG=False            # Desactivar debug
SECRET_KEY=clave_segura # Clave de Flask
```

## 🎮 Características en Producción

- ✅ **SSL automático** (HTTPS)
- ✅ **Dominio personalizable**
- ✅ **Escalabilidad automática**
- ✅ **Logs en tiempo real**
- ✅ **Zero downtime deployments**
- ✅ **Reconocimiento de gestos optimizado**

## 🌍 Acceso Global

Una vez desplegado, cualquier persona puede:

1. **Abrir la URL** de tu app
2. **Crear salas privadas** para jugar con amigos
3. **Jugar contra IA** inmediatamente
4. **Usar desde móvil o desktop**

## 📱 Sharing

Comparte tu juego:

```
🎮 ¡Juega Selfie vs Selfie conmigo!
🌐 https://tu-proyecto.railway.app
📸 Piedra, papel o tijera con gestos
🤖 Modo IA disponible
```

## 🆘 Troubleshooting

### Errores Comunes

1. **Build failed**: Revisar `requirements.txt`
2. **OpenCV error**: Usar `opencv-python-headless`
3. **Port error**: Railway asigna puerto automáticamente
4. **Memory limit**: Railway Free: 512MB, Pro: más

### Logs

```bash
# Ver logs en Railway
railway logs --follow
```

¡Tu juego estará disponible globalmente en minutos! 🌍🎯
