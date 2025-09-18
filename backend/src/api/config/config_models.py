"""
Modelos Flask-RESTX para configuración avanzada del sistema.

Este módulo define los modelos de datos utilizados por los endpoints
de configuración para validación y documentación automática.
"""

from flask_restx import fields, Model


def create_config_models(api):
    """Crea y registra los modelos de configuración en la API."""
    
    # Modelo para configuración completa
    config_model = api.model('Config', {
        'training': fields.Raw(description='Configuración de entrenamiento'),
        'model': fields.Raw(description='Configuración del modelo'),
        'data': fields.Raw(description='Configuración de datos'),
        'system': fields.Raw(description='Configuración del sistema'),
        'timestamp': fields.String(description='Timestamp de última actualización')
    })
    
    # Modelo para sección de configuración
    config_section_model = api.model('ConfigSection', {
        'section_name': fields.String(required=True, description='Nombre de la sección'),
        'config': fields.Raw(required=True, description='Configuración de la sección')
    })
    
    # Modelo para validación de configuración
    config_validation_model = api.model('ConfigValidation', {
        'is_valid': fields.Boolean(description='Si la configuración es válida'),
        'errors': fields.List(fields.String, description='Lista de errores encontrados'),
        'warnings': fields.List(fields.String, description='Lista de advertencias')
    })
    
    # Modelo para respuesta de health check
    health_response_model = api.model('HealthResponse', {
        'status': fields.String(description='Estado del servicio'),
        'service': fields.String(description='Nombre del servicio'),
        'timestamp': fields.String(description='Timestamp del estado')
    })
    
    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(description='Mensaje de error')
    })
    
    return {
        'config_model': config_model,
        'config_section_model': config_section_model,
        'config_validation_model': config_validation_model,
        'health_response_model': health_response_model,
        'error_response_model': error_response_model
    }