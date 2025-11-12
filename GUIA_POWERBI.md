# Guía de Integración de Power BI con Flask

## 📋 Requisitos Previos

1. Tener un reporte publicado en Power BI Service
2. Tener acceso a Power BI Pro o Premium
3. Cuenta de Azure AD (opcional para autenticación avanzada)

## 🔧 Pasos para Integrar Power BI

### Opción 1: Embed Público (Más Simple - Recomendado para empezar)

#### Paso 1: Publicar tu reporte a la web
1. Abre tu reporte en Power BI Service (https://app.powerbi.com)
2. Ve a `Archivo` → `Insertar informe` → `Publicar en la web (público)`
3. Haz clic en `Crear código para insertar`
4. Copia el código iframe que te proporcionan

#### Paso 2: Método con iframe (Más simple)
Modifica el archivo `templates/dashboard.html` y reemplaza el div `powerbi-report` con:

```html
<iframe 
    width="100%" 
    height="600" 
    src="TU_URL_DE_POWER_BI_AQUI" 
    frameborder="0" 
    allowFullScreen="true">
</iframe>
```

**Ejemplo de URL:**
```
https://app.powerbi.com/view?r=eyJrIjoiXXXXXX...
```

### Opción 2: Embed Seguro con JavaScript SDK (Recomendado para producción)

#### Paso 1: Obtener credenciales de Power BI

1. **Registrar aplicación en Azure AD:**
   - Ve a https://portal.azure.com
   - Navega a `Azure Active Directory` → `Registros de aplicaciones` → `Nuevo registro`
   - Nombre: "Flask Power BI App"
   - Tipo de cuenta: "Solo esta organización"
   - URI de redirección: `http://localhost:5000/callback`
   - Guarda el `Application (client) ID`

2. **Configurar permisos:**
   - En tu app registrada, ve a `Permisos de API`
   - Agregar permiso → `Power BI Service`
   - Selecciona los siguientes permisos delegados:
     - `Report.Read.All`
     - `Dataset.Read.All`
     - `Workspace.Read.All`
   - Haz clic en `Conceder consentimiento de administrador`

3. **Crear un secreto de cliente:**
   - Ve a `Certificados y secretos` → `Nuevo secreto de cliente`
   - Descripción: "Flask App Secret"
   - Guarda el valor del secreto (solo se muestra una vez)

#### Paso 2: Obtener IDs de tu reporte

1. Abre tu reporte en Power BI Service
2. La URL tendrá este formato:
   ```
   https://app.powerbi.com/groups/[GROUP_ID]/reports/[REPORT_ID]/ReportSection
   ```
3. Copia `GROUP_ID` (Workspace ID) y `REPORT_ID`

#### Paso 3: Obtener la Embed URL

1. Ve a tu reporte en Power BI Service
2. Haz clic en `Archivo` → `Insertar informe` → `Sitio web o portal`
3. Copia la URL de embed que se muestra

#### Paso 4: Configurar Flask para autenticación

Crea un nuevo archivo `powerbi_auth.py`:

```python
import requests
import msal

class PowerBIAuth:
    def __init__(self):
        self.client_id = 'TU_CLIENT_ID'
        self.client_secret = 'TU_CLIENT_SECRET'
        self.tenant_id = 'TU_TENANT_ID'
        self.scope = ['https://analysis.windows.net/powerbi/api/.default']
        self.authority = f'https://login.microsoftonline.com/{self.tenant_id}'
        
    def get_access_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Error obteniendo token: {result.get('error_description')}")
    
    def get_embed_token(self, group_id, report_id):
        access_token = self.get_access_token()
        
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        body = {
            'accessLevel': 'View'
        }
        
        response = requests.post(url, json=body, headers=headers)
        
        if response.status_code == 200:
            return response.json()['token']
        else:
            raise Exception(f"Error generando embed token: {response.text}")
```

#### Paso 5: Actualizar app.py

Agrega estas líneas a tu `app.py`:

```python
from powerbi_auth import PowerBIAuth

# Inicializar autenticación
powerbi_auth = PowerBIAuth()

@app.route('/api/powerbi-token')
def get_powerbi_token():
    try:
        token = powerbi_auth.get_embed_token(
            POWERBI_CONFIG['group_id'],
            POWERBI_CONFIG['report_id']
        )
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

#### Paso 6: Actualizar dashboard.html

En el archivo `templates/dashboard.html`, modifica el JavaScript para obtener el token:

```javascript
// Obtener token de autenticación
fetch('/api/powerbi-token')
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // Configuración del embed con token
            const embedConfig = {
                type: 'report',
                id: reportConfig.reportId,
                embedUrl: reportConfig.embedUrl,
                accessToken: data.token,
                tokenType: models.TokenType.Embed,
                settings: {
                    panes: {
                        filters: { expanded: false, visible: true }
                    },
                    background: models.BackgroundType.Transparent
                }
            };
            
            // Embed del reporte
            const powerbi = window['powerbi'];
            const report = powerbi.embed(reportContainer, embedConfig);
        }
    });
```

#### Paso 7: Instalar dependencias adicionales

Agrega a `requirements.txt`:
```
msal==1.25.0
requests==2.31.0
```

## 🚀 Configuración Final en app.py

Actualiza la sección POWERBI_CONFIG con tus valores reales:

```python
POWERBI_CONFIG = {
    'report_id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'group_id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'embed_url': 'https://app.powerbi.com/reportEmbed?reportId=XXX&groupId=YYY'
}
```

## 📊 Mejores Prácticas

1. **Seguridad:**
   - Nunca expongas credenciales en el código
   - Usa variables de entorno para información sensible
   - Implementa autenticación de usuarios en tu app Flask

2. **Rendimiento:**
   - Cachea los tokens de acceso (son válidos por 1 hora)
   - Usa Row-Level Security (RLS) en Power BI si es necesario

3. **UX:**
   - Muestra un loader mientras carga el reporte
   - Maneja errores de carga apropiadamente
   - Optimiza el tamaño del iframe/contenedor

## 🔍 Solución de Problemas Comunes

### Error: "Token inválido"
- Verifica que los permisos estén correctamente configurados en Azure AD
- Asegúrate de que el token no haya expirado

### Error: "Report not found"
- Verifica que el report_id y group_id sean correctos
- Confirma que el usuario tenga acceso al workspace

### El reporte no se muestra
- Abre la consola del navegador para ver errores
- Verifica que la URL de embed sea correcta
- Confirma que el SDK de Power BI se haya cargado

## 📚 Recursos Adicionales

- [Documentación oficial Power BI Embedded](https://learn.microsoft.com/es-es/power-bi/developer/embedded/)
- [Power BI REST API](https://learn.microsoft.com/es-es/rest/api/power-bi/)
- [Power BI JavaScript SDK](https://github.com/microsoft/PowerBI-JavaScript)

## 🎯 Resumen Rápido

Para empezar rápidamente:

1. **Método Simple (iframe):**
   - Publica reporte a la web
   - Copia iframe
   - Pégalo en dashboard.html
   ✅ Listo en 5 minutos

2. **Método Avanzado (SDK + Auth):**
   - Registra app en Azure AD
   - Implementa autenticación
   - Usa JavaScript SDK
   ✅ Más seguro y con más control
