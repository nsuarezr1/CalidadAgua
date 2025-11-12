# Ejemplos de Código - Personalización y Extensión

Este archivo contiene ejemplos prácticos de código que puedes usar para personalizar y extender tu aplicación Flask.

## 📊 1. Conectar con Base de Datos

### Ejemplo con SQLite

```python
# Agregar a app.py
import sqlite3
from datetime import datetime

def init_db():
    """Inicializar base de datos"""
    conn = sqlite3.connect('calidad_agua.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departamento TEXT NOT NULL,
            fecha DATE NOT NULL,
            ph REAL,
            turbidez REAL,
            temperatura REAL,
            calidad_score INTEGER,
            estado TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def obtener_datos_db():
    """Obtener datos de calidad de agua desde la base de datos"""
    conn = sqlite3.connect('calidad_agua.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT departamento, AVG(calidad_score) as calidad, estado
        FROM mediciones
        GROUP BY departamento
        ORDER BY calidad DESC
    ''')
    
    resultados = cursor.fetchall()
    conn.close()
    
    return [
        {
            'nombre': row[0],
            'calidad': int(row[1]),
            'estado': row[2]
        }
        for row in resultados
    ]

# Actualizar el endpoint de API
@app.route('/api/calidad-agua')
def api_calidad_agua():
    datos = obtener_datos_db()
    return jsonify({'departamentos': datos})
```

### Ejemplo con PostgreSQL

```python
# requirements.txt
# psycopg2-binary==2.9.9

import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Crear conexión a PostgreSQL"""
    conn = psycopg2.connect(
        host="localhost",
        database="calidad_agua",
        user="tu_usuario",
        password="tu_password"
    )
    return conn

@app.route('/api/calidad-agua')
def api_calidad_agua():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute('''
        SELECT 
            departamento as nombre,
            AVG(calidad_score) as calidad,
            estado
        FROM mediciones
        WHERE fecha >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY departamento, estado
        ORDER BY calidad DESC
    ''')
    
    departamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({'departamentos': departamentos})
```

## 🔐 2. Autenticación de Usuarios

### Login Simple con Flask-Login

```python
# requirements.txt
# Flask-Login==0.6.3

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo de Usuario
class Usuario(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    # Aquí buscarías el usuario en tu base de datos
    # Este es solo un ejemplo
    if user_id == "1":
        return Usuario(1, "admin", "admin@ejemplo.com")
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verificar credenciales (conectar con tu DB)
        if username == "admin" and password == "admin123":
            user = Usuario(1, username, "admin@ejemplo.com")
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Proteger rutas
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

## 📧 3. Envío de Alertas por Email

```python
# requirements.txt
# Flask-Mail==0.9.1

from flask_mail import Mail, Message

# Configuración de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_password'

mail = Mail(app)

def enviar_alerta_calidad(departamento, calidad):
    """Enviar alerta si la calidad del agua es baja"""
    if calidad < 50:
        msg = Message(
            f'Alerta: Baja calidad de agua en {departamento}',
            sender='tu_email@gmail.com',
            recipients=['destinatario@ejemplo.com']
        )
        msg.body = f'''
        Se ha detectado baja calidad de agua en {departamento}.
        
        Calidad actual: {calidad}%
        Estado: Crítico
        
        Se requiere atención inmediata.
        '''
        mail.send(msg)

# Usar en tu endpoint
@app.route('/api/verificar-calidad')
def verificar_calidad():
    datos = obtener_datos_db()
    for dept in datos:
        enviar_alerta_calidad(dept['nombre'], dept['calidad'])
    return jsonify({'mensaje': 'Verificación completada'})
```

## 📈 4. Gráficos Adicionales con Chart.js

```html
<!-- En dashboard.html -->
<canvas id="calidadChart" width="400" height="200"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
async function cargarGrafico() {
    const response = await fetch('/api/calidad-agua');
    const data = await response.json();
    
    const ctx = document.getElementById('calidadChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.departamentos.map(d => d.nombre),
            datasets: [{
                label: 'Calidad del Agua (%)',
                data: data.departamentos.map(d => d.calidad),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(153, 102, 255, 0.6)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

cargarGrafico();
</script>
```

## 🗺️ 5. Mapa Interactivo con Leaflet

```html
<!-- Agregar a dashboard.html -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div id="mapa" style="height: 500px;"></div>

<script>
// Inicializar mapa centrado en Colombia
const mapa = L.map('mapa').setView([4.5709, -74.2973], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(mapa);

// Coordenadas de departamentos (ejemplos)
const ubicaciones = {
    'Antioquia': [6.2476, -75.5658],
    'Cundinamarca': [4.7110, -74.0721],
    'Valle del Cauca': [3.4516, -76.5320],
    'Atlántico': [10.9639, -74.7964],
    'Santander': [7.1254, -73.1198]
};

// Cargar datos y agregar marcadores
fetch('/api/calidad-agua')
    .then(response => response.json())
    .then(data => {
        data.departamentos.forEach(dept => {
            if (ubicaciones[dept.nombre]) {
                const [lat, lng] = ubicaciones[dept.nombre];
                
                // Color según calidad
                const color = dept.calidad >= 80 ? 'green' : 
                             dept.calidad >= 60 ? 'orange' : 'red';
                
                const marker = L.circleMarker([lat, lng], {
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.7,
                    radius: 10
                }).addTo(mapa);
                
                marker.bindPopup(`
                    <b>${dept.nombre}</b><br>
                    Calidad: ${dept.calidad}%<br>
                    Estado: ${dept.estado}
                `);
            }
        });
    });
</script>
```

## ⏱️ 6. Actualización en Tiempo Real con WebSockets

```python
# requirements.txt
# Flask-SocketIO==5.3.5

from flask_socketio import SocketIO, emit
import threading
import time

socketio = SocketIO(app)

def actualizar_datos_periodicamente():
    """Enviar actualizaciones cada 30 segundos"""
    while True:
        time.sleep(30)
        datos = obtener_datos_db()
        socketio.emit('actualizacion_datos', datos)

# Iniciar thread de actualización
thread = threading.Thread(target=actualizar_datos_periodicamente)
thread.daemon = True
thread.start()

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    datos = obtener_datos_db()
    emit('datos_iniciales', datos)

# En index.html
"""
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
    const socket = io();
    
    socket.on('datos_iniciales', function(datos) {
        console.log('Datos iniciales recibidos:', datos);
        actualizarInterfaz(datos);
    });
    
    socket.on('actualizacion_datos', function(datos) {
        console.log('Actualización recibida:', datos);
        actualizarInterfaz(datos);
    });
    
    function actualizarInterfaz(datos) {
        // Actualizar la interfaz con los nuevos datos
        const container = document.getElementById('stats-container');
        // ... tu código de actualización ...
    }
</script>
"""
```

## 📊 7. Exportar Datos a Excel

```python
# requirements.txt
# openpyxl==3.1.2

from flask import send_file
from openpyxl import Workbook
from datetime import datetime
import io

@app.route('/exportar/excel')
def exportar_excel():
    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Calidad Agua"
    
    # Headers
    ws['A1'] = 'Departamento'
    ws['B1'] = 'Calidad (%)'
    ws['C1'] = 'Estado'
    ws['D1'] = 'Fecha Reporte'
    
    # Datos
    datos = obtener_datos_db()
    for idx, dept in enumerate(datos, start=2):
        ws[f'A{idx}'] = dept['nombre']
        ws[f'B{idx}'] = dept['calidad']
        ws[f'C{idx}'] = dept['estado']
        ws[f'D{idx}'] = datetime.now().strftime('%Y-%m-%d')
    
    # Guardar en memoria
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'calidad_agua_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )
```

## 🔍 8. Búsqueda y Filtrado Avanzado

```python
@app.route('/api/calidad-agua/filtrar')
def filtrar_calidad():
    # Obtener parámetros de query
    min_calidad = request.args.get('min_calidad', 0, type=int)
    max_calidad = request.args.get('max_calidad', 100, type=int)
    estado = request.args.get('estado', None)
    departamento = request.args.get('departamento', None)
    
    conn = sqlite3.connect('calidad_agua.db')
    cursor = conn.cursor()
    
    query = '''
        SELECT departamento, calidad_score, estado
        FROM mediciones
        WHERE calidad_score BETWEEN ? AND ?
    '''
    params = [min_calidad, max_calidad]
    
    if estado:
        query += ' AND estado = ?'
        params.append(estado)
    
    if departamento:
        query += ' AND departamento LIKE ?'
        params.append(f'%{departamento}%')
    
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'departamentos': [
            {
                'nombre': r[0],
                'calidad': r[1],
                'estado': r[2]
            }
            for r in resultados
        ]
    })
```

## 🔔 9. Sistema de Notificaciones Push

```python
# requirements.txt
# pywebpush==1.14.0

from pywebpush import webpush, WebPushException
import json

# Almacenar suscripciones (en producción usar DB)
suscripciones = []

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Registrar suscripción a notificaciones push"""
    subscription = request.json
    suscripciones.append(subscription)
    return jsonify({'success': True})

def enviar_notificacion_push(titulo, mensaje):
    """Enviar notificación push a todos los suscriptores"""
    for subscription in suscripciones:
        try:
            webpush(
                subscription_info=subscription,
                data=json.dumps({
                    'title': titulo,
                    'body': mensaje,
                    'icon': '/static/icon.png'
                }),
                vapid_private_key="TU_PRIVATE_KEY",
                vapid_claims={
                    "sub": "mailto:tu_email@ejemplo.com"
                }
            )
        except WebPushException as e:
            print(f"Error enviando notificación: {e}")
```

## 🎨 10. Modo Oscuro

```css
/* Agregar a style.css */

/* Variables CSS */
:root {
    --bg-color: #f4f7f9;
    --text-color: #333;
    --card-bg: white;
    --primary-color: #1565c0;
}

[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
    --card-bg: #2d2d2d;
    --primary-color: #42a5f5;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}

.feature-card, .stat-card {
    background: var(--card-bg);
}

/* Toggle switch */
.theme-switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}
```

```javascript
// Agregar a templates/base.html
<script>
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Cargar tema guardado
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
</script>
```

## 🚀 Estos ejemplos te ayudarán a:

1. ✅ Conectar con bases de datos reales
2. ✅ Implementar autenticación de usuarios
3. ✅ Enviar alertas automáticas
4. ✅ Crear visualizaciones interactivas
5. ✅ Agregar mapas geográficos
6. ✅ Actualizar datos en tiempo real
7. ✅ Exportar reportes a Excel
8. ✅ Filtrar y buscar datos
9. ✅ Enviar notificaciones push
10. ✅ Implementar modo oscuro

Elige los que necesites y adáptalos a tu proyecto. ¡Buena suerte! 🎉
