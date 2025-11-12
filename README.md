# Sistema de Monitoreo de Calidad de Agua en Colombia 💧

Aplicación Flask para visualizar y analizar datos de calidad de agua en Colombia, integrada con reportes de Power BI.

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd proyecto-calidad-agua
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🏃 Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
proyecto-calidad-agua/
│
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias Python
├── GUIA_POWERBI.md            # Guía detallada de integración Power BI
├── README.md                   # Este archivo
│
├── templates/                  # Plantillas HTML
│   ├── base.html              # Plantilla base
│   ├── index.html             # Página principal
│   ├── dashboard.html         # Dashboard Power BI
│   └── about.html             # Acerca del proyecto
│
└── static/                     # Archivos estáticos
    ├── css/
    │   └── style.css          # Estilos CSS
    └── js/
        └── (archivos JS adicionales)
```

## 🔧 Configuración de Power BI

### Opción 1: Embed Público (Rápido)

1. Publica tu reporte en Power BI Service
2. Ve a `Archivo` → `Publicar en la web`
3. Copia el código iframe
4. Edita `templates/dashboard.html` y reemplaza el contenido del div `powerbi-report` con tu iframe

### Opción 2: Embed Seguro (Recomendado)

Lee la guía completa en `GUIA_POWERBI.md` para configurar:
- Registro de aplicación en Azure AD
- Autenticación con tokens
- JavaScript SDK de Power BI

## 📊 Endpoints de la API

- `GET /` - Página principal
- `GET /dashboard` - Dashboard con Power BI
- `GET /about` - Información del proyecto
- `GET /api/calidad-agua` - API JSON con datos de calidad de agua

### Ejemplo de respuesta de la API:

```json
{
  "departamentos": [
    {
      "nombre": "Antioquia",
      "calidad": 85,
      "estado": "Buena"
    },
    ...
  ]
}
```

## 🎨 Personalización

### Modificar colores y estilos

Edita el archivo `static/css/style.css`

### Agregar más departamentos

Modifica la función `api_calidad_agua()` en `app.py`

### Cambiar datos mostrados

Actualiza los templates en la carpeta `templates/`

## 📝 Notas de Desarrollo

- La aplicación usa Flask en modo debug (solo para desarrollo)
- Para producción, usa un servidor WSGI como Gunicorn
- Los datos de ejemplo están hardcoded en `app.py`
- Para datos reales, conecta con una base de datos

## 🔐 Variables de Entorno (Producción)

Para producción, usa variables de entorno para información sensible:

```python
import os

POWERBI_CONFIG = {
    'report_id': os.getenv('POWERBI_REPORT_ID'),
    'group_id': os.getenv('POWERBI_GROUP_ID'),
    'embed_url': os.getenv('POWERBI_EMBED_URL')
}
```

## 🚢 Despliegue

### Opción 1: Heroku

```bash
# Crear Procfile
echo "web: gunicorn app:app" > Procfile

# Agregar gunicorn a requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Deploy
git init
heroku create mi-app-calidad-agua
git add .
git commit -m "Initial commit"
git push heroku master
```

### Opción 2: PythonAnywhere

1. Sube los archivos a PythonAnywhere
2. Configura una nueva Web App con Flask
3. Configura el WSGI file para apuntar a tu app.py

### Opción 3: Azure App Service

1. Instala Azure CLI
2. Ejecuta:
```bash
az webapp up --name mi-app-calidad-agua --sku B1
```

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de adaptarlo a tus necesidades.

## 📚 Recursos Adicionales

- [Documentación Flask](https://flask.palletsprojects.com/)
- [Power BI Embedded](https://learn.microsoft.com/es-es/power-bi/developer/embedded/)
- [Guía de integración Power BI](./GUIA_POWERBI.md)

## 📞 Soporte

Para dudas sobre:
- **Flask**: Consulta la documentación oficial
- **Power BI**: Lee la guía GUIA_POWERBI.md
- **Integración**: Revisa los comentarios en el código

## ✅ Checklist de Implementación

- [ ] Instalar dependencias
- [ ] Ejecutar la aplicación localmente
- [ ] Crear reporte en Power BI
- [ ] Publicar reporte a Power BI Service
- [ ] Configurar integración (iframe o SDK)
- [ ] Probar dashboard
- [ ] Personalizar estilos y contenido
- [ ] Agregar datos reales
- [ ] Configurar para producción
- [ ] Desplegar

¡Buena suerte con tu proyecto! 🚀
