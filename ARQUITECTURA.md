# Arquitectura del Sistema - Calidad de Agua Colombia

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO / NAVEGADOR                      │
│                     http://localhost:5000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APLICACIÓN FLASK                            │
│                         (app.py)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  RUTAS (Routes):                                                 │
│  ┌───────────────────────────────────────────────────┐          │
│  │  GET /              → index.html                   │          │
│  │  GET /dashboard     → dashboard.html               │          │
│  │  GET /about         → about.html                   │          │
│  │  GET /api/calidad-agua → JSON API                  │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                   │
│  AUTENTICACIÓN POWER BI (powerbi_auth.py):                      │
│  ┌───────────────────────────────────────────────────┐          │
│  │  - Obtener access token de Azure AD               │          │
│  │  - Generar embed token para reportes              │          │
│  │  - Cache de tokens (1 hora)                       │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                   │
└────────────────┬─────────────────────┬──────────────────────────┘
                 │                     │
                 │                     │
    ┌────────────▼─────────┐  ┌────────▼──────────────────┐
    │   TEMPLATES HTML     │  │   ARCHIVOS ESTÁTICOS      │
    │                      │  │                            │
    │  - base.html         │  │  - CSS (style.css)        │
    │  - index.html        │  │  - JavaScript             │
    │  - dashboard.html    │  │  - Imágenes               │
    │  - about.html        │  │                            │
    └──────────────────────┘  └───────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRACIÓN POWER BI                          │
└─────────────────────────────────────────────────────────────────┘

Opción A: EMBED PÚBLICO (Simple)
────────────────────────────────
┌──────────────┐     Iframe      ┌─────────────────┐
│   Browser    │ ───────────────►│  Power BI       │
│  (Cliente)   │                 │  Service        │
└──────────────┘                 │  (Reporte)      │
                                 └─────────────────┘

Opción B: EMBED SEGURO (Avanzado)
──────────────────────────────────
┌──────────────┐   1. Request    ┌─────────────────┐
│   Browser    │ ───────────────►│  Flask App      │
│  (Cliente)   │                 │  (Backend)      │
└──────────────┘                 └────────┬────────┘
       ▲                                  │
       │                                  │ 2. Get Token
       │                                  ▼
       │                         ┌─────────────────┐
       │                         │   Azure AD      │
       │                         │  (Auth Server)  │
       │                         └────────┬────────┘
       │                                  │
       │                                  │ 3. Access Token
       │                                  ▼
       │                         ┌─────────────────┐
       │                         │  Power BI API   │
       │ 4. Embed Token         │                 │
       └─────────────────────────┤  Generate       │
                                 │  Embed Token    │
                                 └────────┬────────┘
                                          │
                                          │ 5. Embed Token
                                          ▼
       ┌──────────────┐          ┌─────────────────┐
       │   Browser    │ 6. Load  │  Power BI       │
       │  + Token     │ ────────►│  Service        │
       │              │          │  (Reporte)      │
       └──────────────┘          └─────────────────┘


## 🔄 Flujo de Datos

### Flujo 1: Cargar Página Principal
```
Usuario → GET / → Flask Router → Renderizar index.html
                                      ↓
                                 JavaScript carga datos
                                      ↓
                                 GET /api/calidad-agua
                                      ↓
                                 Flask devuelve JSON
                                      ↓
                                 Renderizar tarjetas en pantalla
```

### Flujo 2: Cargar Dashboard Power BI (Método Seguro)
```
Usuario → GET /dashboard → Flask renderiza dashboard.html
                                      ↓
                           JavaScript se carga en navegador
                                      ↓
                           fetch('/api/powerbi-token')
                                      ↓
                           Flask ejecuta powerbi_auth.py
                                      ↓
                           Obtener access token de Azure AD
                                      ↓
                           Generar embed token con Power BI API
                                      ↓
                           Devolver token al navegador
                                      ↓
                           Power BI SDK embed el reporte
```

### Flujo 3: API de Datos
```
Cliente → GET /api/calidad-agua → Flask procesa request
                                       ↓
                                  Consulta datos (actualmente hardcoded)
                                       ↓
                                  Formato JSON
                                       ↓
                                  jsonify(datos)
                                       ↓
                                  Respuesta HTTP 200 con JSON
```

## 🗂️ Estructura de Datos

### Configuración Power BI
```python
POWERBI_CONFIG = {
    'report_id': 'UUID del reporte',
    'group_id': 'UUID del workspace',
    'embed_url': 'https://app.powerbi.com/reportEmbed?...'
}
```

### Respuesta API Calidad Agua
```json
{
  "departamentos": [
    {
      "nombre": "string",
      "calidad": number (0-100),
      "estado": "Excelente|Buena|Aceptable|Mala"
    }
  ]
}
```

### Token de Power BI (Respuesta)
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "tokenId": "UUID",
  "expiration": "2024-11-11T18:00:00Z"
}
```

## 🔐 Seguridad

### Variables de Entorno (Recomendado)
```python
import os

CLIENT_ID = os.getenv('POWERBI_CLIENT_ID')
CLIENT_SECRET = os.getenv('POWERBI_CLIENT_SECRET')
TENANT_ID = os.getenv('POWERBI_TENANT_ID')
```

### Configuración .env
```bash
POWERBI_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
POWERBI_CLIENT_SECRET=tu_secreto_aqui
POWERBI_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
POWERBI_GROUP_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
POWERBI_REPORT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## 🚀 Despliegue

### Desarrollo
```
Python Built-in Server
Port: 5000
Debug: True
Host: localhost
```

### Producción
```
WSGI Server (Gunicorn/uWSGI)
Port: 80/443
Debug: False
Host: 0.0.0.0
Reverse Proxy: Nginx
SSL: Let's Encrypt
```

## 📊 Componentes Principales

1. **Flask Backend (app.py)**
   - Servidor web
   - Routing
   - API REST
   - Integración con Power BI

2. **Power BI Auth (powerbi_auth.py)**
   - Autenticación Azure AD
   - Gestión de tokens
   - Cache de credenciales

3. **Frontend (Templates + CSS)**
   - Interfaz de usuario
   - Visualización de datos
   - Integración Power BI SDK

4. **API REST**
   - Endpoint de datos
   - Formato JSON
   - CORS habilitado (si es necesario)

## 🔌 APIs Externas Utilizadas

- **Azure AD API**: Autenticación
- **Power BI REST API**: Embed tokens, reportes
- **Power BI JavaScript SDK**: Visualización de reportes

## 📈 Escalabilidad

### Actual (Desarrollo)
- 1 instancia Flask
- Sin base de datos
- Datos hardcoded

### Futuro (Producción)
- Múltiples workers Gunicorn
- Base de datos PostgreSQL/MySQL
- Cache Redis para tokens
- Load balancer
- CDN para archivos estáticos

## 🎯 Puntos de Extensión

1. **Base de Datos**: Agregar PostgreSQL para datos reales
2. **Autenticación**: Implementar login de usuarios
3. **Cache**: Redis para tokens y datos frecuentes
4. **Monitoring**: Agregar logging y métricas
5. **Testing**: Unit tests y integration tests
6. **CI/CD**: Pipeline automatizado de despliegue
