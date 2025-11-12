"""
Módulo de autenticación para Power BI
Este archivo proporciona funcionalidad para autenticación con Azure AD
y generación de tokens de embed para Power BI
"""

import requests
import msal
from datetime import datetime, timedelta

class PowerBIAuth:
    """
    Clase para manejar la autenticación con Power BI Service
    """
    
    def __init__(self, client_id, client_secret, tenant_id):
        """
        Inicializar configuración de autenticación
        
        Args:
            client_id: Application (client) ID de Azure AD
            client_secret: Client secret de la aplicación
            tenant_id: Tenant ID de Azure AD
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.scope = ['https://analysis.windows.net/powerbi/api/.default']
        self.authority = f'https://login.microsoftonline.com/{tenant_id}'
        
        # Cache para el token
        self.cached_token = None
        self.token_expiry = None
        
    def get_access_token(self):
        """
        Obtener token de acceso de Azure AD
        
        Returns:
            str: Access token para Power BI API
        """
        # Verificar si hay token en cache y si aún es válido
        if self.cached_token and self.token_expiry:
            if datetime.now() < self.token_expiry:
                return self.cached_token
        
        # Crear aplicación MSAL
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        # Adquirir token
        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            self.cached_token = result["access_token"]
            # El token expira en aproximadamente 1 hora
            self.token_expiry = datetime.now() + timedelta(minutes=55)
            return result["access_token"]
        else:
            error_msg = result.get('error_description', 'Error desconocido')
            raise Exception(f"Error obteniendo access token: {error_msg}")
    
    def get_embed_token(self, group_id, report_id, datasets=None):
        """
        Generar token de embed para un reporte específico
        
        Args:
            group_id: ID del workspace de Power BI
            report_id: ID del reporte
            datasets: Lista de IDs de datasets (opcional)
            
        Returns:
            dict: Información del embed token incluyendo token, expiry, etc.
        """
        access_token = self.get_access_token()
        
        # URL del API para generar token
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        # Body de la solicitud
        body = {
            'accessLevel': 'View',
            'allowSaveAs': False
        }
        
        # Si se proporcionan datasets, agregarlos
        if datasets:
            body['datasets'] = [{'id': ds_id} for ds_id in datasets]
        
        # Hacer la solicitud
        response = requests.post(url, json=body, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.text
            raise Exception(f"Error generando embed token: {error_msg}")
    
    def get_report_info(self, group_id, report_id):
        """
        Obtener información de un reporte
        
        Args:
            group_id: ID del workspace
            report_id: ID del reporte
            
        Returns:
            dict: Información del reporte
        """
        access_token = self.get_access_token()
        
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}'
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error obteniendo información del reporte: {response.text}")
    
    def get_datasets_in_group(self, group_id):
        """
        Listar todos los datasets en un workspace
        
        Args:
            group_id: ID del workspace
            
        Returns:
            list: Lista de datasets
        """
        access_token = self.get_access_token()
        
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets'
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            raise Exception(f"Error obteniendo datasets: {response.text}")


# Ejemplo de uso
if __name__ == '__main__':
    # Configuración (reemplazar con valores reales)
    CLIENT_ID = 'tu-client-id'
    CLIENT_SECRET = 'tu-client-secret'
    TENANT_ID = 'tu-tenant-id'
    GROUP_ID = 'tu-group-id'
    REPORT_ID = 'tu-report-id'
    
    # Crear instancia de autenticación
    auth = PowerBIAuth(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
    
    try:
        # Obtener token de embed
        embed_info = auth.get_embed_token(GROUP_ID, REPORT_ID)
        print("Token obtenido exitosamente:")
        print(f"Token: {embed_info['token'][:50]}...")
        print(f"Token ID: {embed_info['tokenId']}")
        print(f"Expira: {embed_info['expiration']}")
        
        # Obtener información del reporte
        report_info = auth.get_report_info(GROUP_ID, REPORT_ID)
        print(f"\nReporte: {report_info['name']}")
        print(f"Embed URL: {report_info['embedUrl']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
