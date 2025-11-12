# 🚀 INICIO RÁPIDO - Proyecto Calidad de Agua Colombia

## 📦 Lo que acabas de recibir

Una aplicación Flask completa con:
- ✅ Backend Flask funcional
- ✅ Frontend responsive con 3 páginas
- ✅ API REST para datos de calidad de agua
- ✅ Integración lista para Power BI
- ✅ Documentación completa

## ⚡ Primeros Pasos (5 minutos)

### 1. Instalar y ejecutar

```bash
# Instalar Flask
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

Abre tu navegador en: http://localhost:5000

### 2. Ver la aplicación funcionando

Ya puedes ver:
- **Página principal** con información del proyecto
- **API funcionando** en /api/calidad-agua
- **Página "Acerca de"** con detalles del proyecto
- **Dashboard** listo para integrar Power BI

## 🎯 Integrar Power BI (2 opciones)

### Opción A: RÁPIDA (5 minutos) - Recomendada para empezar

1. Ve a Power BI Service (https://app.powerbi.com)
2. Abre tu reporte de calidad de agua
3. Click en: `Archivo` → `Publicar en la web (público)`
4. Copia el código `<iframe>` que te dan
5. Edita `templates/dashboard.html` línea 17
6. Reemplaza el `<div id="powerbi-report">` con tu iframe
7. ¡Listo! Recarga la página

**Ejemplo:**
```html
<iframe 
    width="100%" 
    height="600" 
    src="https://app.powerbi.com/view?r=eyJrIjoiXXX..." 
    frameborder="0" 
    allowFullScreen="true">
</iframe>
```

### Opción B: SEGURA (30 minutos) - Para producción

Lee la guía completa en: `GUIA_POWERBI.md`

Incluye:
- Autenticación con Azure AD
- Tokens de seguridad
- Control de acceso
- JavaScript SDK

## 📁 Estructura de Archivos

```
📦 proyecto-calidad-agua/
│
├── 📄 app.py                    # ← Aplicación Flask principal
├── 📄 powerbi_auth.py           # ← Autenticación Power BI (avanzado)
├── 📄 requirements.txt          # ← Dependencias Python
│
├── 📘 README.md                 # ← Documentación general
├── 📘 GUIA_POWERBI.md          # ← Guía detallada Power BI
├── 📘 INICIO_RAPIDO.md         # ← Este archivo
│
├── 📁 templates/                # ← Páginas HTML
│   ├── base.html               # Plantilla base
│   ├── index.html              # Página principal
│   ├── dashboard.html          # Dashboard Power BI
│   └── about.html              # Acerca de
│
└── 📁 static/                   # ← Estilos
    └── css/
        └── style.css           # Diseño completo
```

## 🔧 Configuración en app.py

Para usar la Opción B (segura), edita en `app.py`:

```python
POWERBI_CONFIG = {
    'report_id': 'pon-aqui-tu-report-id',
    'group_id': 'pon-aqui-tu-workspace-id',
    'embed_url': 'pon-aqui-tu-embed-url'
}
```

**¿Dónde encontrar estos valores?**
- Abre tu reporte en Power BI Service
- La URL tiene este formato:
  `https://app.powerbi.com/groups/[GROUP_ID]/reports/[REPORT_ID]/...`
- Copia esos IDs

## 🎨 Personalización Rápida

### Cambiar colores
Edita `static/css/style.css` líneas 35-36:
```css
background: linear-gradient(135deg, #TU_COLOR_1, #TU_COLOR_2);
```

### Agregar más departamentos
Edita `app.py` función `api_calidad_agua()` línea 20:
```python
{'nombre': 'Nuevo Departamento', 'calidad': 90, 'estado': 'Excelente'}
```

### Cambiar título
Edita `templates/base.html` línea 11:
```html
<h2>💧 Tu Título Aquí</h2>
```

## 📊 API Endpoints

Tu aplicación ya tiene una API REST funcionando:

```
GET /                      → Página principal
GET /dashboard            → Dashboard Power BI
GET /about                → Información del proyecto
GET /api/calidad-agua     → JSON con datos
```

**Prueba la API:**
```bash
curl http://localhost:5000/api/calidad-agua
```

## ✅ Checklist de Implementación

- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Ejecutar app: `python app.py`
- [ ] Verificar que funciona: http://localhost:5000
- [ ] Tener reporte publicado en Power BI Service
- [ ] Elegir método de integración (A o B)
- [ ] Configurar Power BI según método elegido
- [ ] Probar dashboard con tu reporte
- [ ] Personalizar textos y colores
- [ ] (Opcional) Agregar datos reales
- [ ] (Opcional) Preparar para producción

## 🆘 Solución de Problemas

### "No module named 'flask'"
```bash
pip install flask
```

### "ModuleNotFoundError: No module named 'werkzeug'"
```bash
pip install werkzeug
```

### Power BI no se muestra
1. Verifica que copiaste correctamente el iframe/configuración
2. Abre la consola del navegador (F12) para ver errores
3. Asegúrate de que el reporte esté publicado
4. Confirma que la URL de embed es correcta

### Error al ejecutar app.py
- Verifica que estés en la carpeta correcta
- Asegúrate de tener Python 3.7 o superior
- Instala todas las dependencias

## 🎓 Próximos Pasos

1. **Funcionamiento básico** ✅ Ya lo tienes
2. **Integrar Power BI** → Sigue una de las opciones arriba
3. **Conectar datos reales** → Agrega base de datos
4. **Mejorar seguridad** → Autenticación de usuarios
5. **Desplegar online** → Heroku, Azure, PythonAnywhere

## 📚 Documentación Adicional

- **README.md** - Información completa del proyecto
- **GUIA_POWERBI.md** - Guía detallada de integración Power BI
- **Comentarios en código** - Explicaciones en cada archivo

## 💡 Tips Profesionales

1. **Durante desarrollo:** Usa debug=True (ya configurado)
2. **Para producción:** Cambia a debug=False y usa Gunicorn
3. **Seguridad:** Usa variables de entorno para credenciales
4. **Performance:** Implementa cache para tokens de Power BI

## 🎉 ¡Listo!

Tu aplicación Flask está completa y lista para usar. Solo necesitas:
1. Ejecutarla (`python app.py`)
2. Integrar tu reporte de Power BI
3. Personalizarla a tu gusto

**¿Necesitas ayuda?** Revisa:
- README.md para documentación general
- GUIA_POWERBI.md para integración Power BI
- Comentarios en el código fuente

---
**Proyecto:** Sistema de Monitoreo de Calidad de Agua en Colombia
**Tecnologías:** Flask, Power BI, HTML/CSS/JavaScript
**Versión:** 1.0
