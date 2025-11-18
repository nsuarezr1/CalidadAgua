from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Configuración para Power BI
# Estos valores los obtendrás de Power BI Service
POWERBI_CONFIG = {
    'report_id': 'TU_REPORT_ID',  # ID del reporte
    'group_id': 'TU_GROUP_ID',    # ID del workspace
    'embed_url': 'TU_EMBED_URL'   # URL de embed del reporte
}

@app.route('/')
def index():
    """Página principal con dashboard de calidad de agua"""
    return render_template('index.html', title='Calidad de Agua en Colombia')

@app.route('/dashboard')
def dashboard():
    """Página con el reporte de Power BI embebido"""
    return render_template('dashboard.html', 
                         title='Dashboard - Calidad de Agua',
                         powerbi_config=POWERBI_CONFIG)

@app.route('/api/calidad-agua')
def api_calidad_agua():
    """API endpoint para datos de calidad de agua"""
    # Aquí puedes conectar con tu base de datos o fuente de datos
    datos_ejemplo = {
        'departamentos': [
            {'nombre': 'Antioquia', 'calidad': 85, 'estado': 'Buena'},
            {'nombre': 'Cundinamarca', 'calidad': 78, 'estado': 'Aceptable'},
            {'nombre': 'Valle del Cauca', 'calidad': 82, 'estado': 'Buena'},
            {'nombre': 'Atlántico', 'calidad': 70, 'estado': 'Aceptable'},
            {'nombre': 'Santander', 'calidad': 88, 'estado': 'Excelente'}
        ]
    }
    return jsonify(datos_ejemplo)

@app.route('/about')
def about():
    """Página sobre el proyecto"""
    return render_template('about.html', title='Sobre el Proyecto')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
