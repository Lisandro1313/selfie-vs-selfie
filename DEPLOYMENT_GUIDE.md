# 🚂 Guía de Deployment: Selfie vs Selfie en Railway

## Archivos preparados para deployment:

✅ `requirements.txt` - Dependencias de Python
✅ `Procfile` - Comando de inicio para Railway
✅ `app.py` - Configurado con variables de entorno
✅ `.gitignore` - Archivos a excluir del repositorio

## 🎯 Pasos para subir a Railway:

### 1. Crear cuenta en Railway

- Ir a https://railway.app/
- Registrarse con GitHub (recomendado)

### 2. Subir código a GitHub

```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "🏖️ Selfie vs Selfie - Juego completo con estética Playa del Carmen"

# Crear repositorio en GitHub y conectar
# (seguir instrucciones de GitHub)
git remote add origin https://github.com/TU_USUARIO/selfie-vs-selfie.git
git push -u origin main
```

### 3. Deployment en Railway

1. **Login en Railway** con tu cuenta de GitHub
2. **New Project** → **Deploy from GitHub repo**
3. **Seleccionar** tu repositorio `selfie-vs-selfie`
4. **Railway detectará automáticamente** que es una app Python
5. **Deploy** automático comenzará

### 4. Configuración automática

- Railway leerá `requirements.txt` e instalará dependencias
- Usará `Procfile` para saber cómo ejecutar la app
- Asignará un puerto automáticamente
- Generará una URL pública

### 5. Variables de entorno (si es necesario)

En el dashboard de Railway:

- **Variables** → **New Variable**
- `FLASK_ENV` = `production` (opcional)

## 🌐 Resultado final:

- Tu app estará disponible en: `https://tu-app.railway.app`
- Acceso global 24/7
- SSL automático
- Escalado automático

## 🎮 Funcionalidades online:

✅ **Multijugador real** - Crear salas y esperar jugadores
✅ **Modo IA** - Jugar solo cuando no hay nadie online  
✅ **Detección de gestos** - Funciona con cualquier webcam
✅ **Estética Playa del Carmen** - Diseño tropical completo

## 📱 Compatibilidad:

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Mobile (navegadores móviles con cámara)
- ✅ Tablets
- ✅ Funciona globalmente

## 🔧 Troubleshooting:

- **Build falla**: Verificar que `requirements.txt` esté correcto
- **App no inicia**: Revisar logs en Railway dashboard
- **Cámara no funciona**: Usuario debe dar permisos de cámara

## 💡 Tips:

- Railway tiene plan gratuito generoso
- Los deploys son automáticos con cada push a main
- Puedes ver logs en tiempo real en el dashboard
- El dominio se puede personalizar en el plan pago
