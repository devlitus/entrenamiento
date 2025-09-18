# backend/src/api/realtime_models.py
"""
Modelos de datos para endpoints de tiempo real usando Flask-RESTX.

Este módulo define los modelos de datos para la documentación Swagger
de los endpoints de comunicación en tiempo real.
"""

from flask_restx import fields

def create_realtime_models(api):
    """Crea y retorna los modelos de datos para endpoints de tiempo real"""
    
    # Modelo para configuración de conexión
    connection_config_model = api.model('ConnectionConfig', {
        'client_id': fields.String(required=True, description='ID único del cliente'),
        'channels': fields.List(fields.String, description='Canales a suscribir'),
        'heartbeat_interval': fields.Integer(default=30, description='Intervalo de heartbeat en segundos')
    })
    
    # Modelo para evento de progreso de entrenamiento
    training_progress_model = api.model('TrainingProgress', {
        'experiment_id': fields.String(required=True, description='ID del experimento'),
        'epoch': fields.Integer(required=True, description='Época actual'),
        'total_epochs': fields.Integer(required=True, description='Total de épocas'),
        'loss': fields.Float(description='Pérdida actual'),
        'accuracy': fields.Float(description='Precisión actual'),
        'val_loss': fields.Float(description='Pérdida de validación'),
        'val_accuracy': fields.Float(description='Precisión de validación'),
        'timestamp': fields.String(required=True, description='Timestamp del evento'),
        'status': fields.String(enum=['training', 'completed', 'error'], description='Estado del entrenamiento')
    })
    
    # Modelo para evento de sistema
    system_event_model = api.model('SystemEvent', {
        'event_type': fields.String(required=True, enum=['info', 'warning', 'error'], description='Tipo de evento'),
        'message': fields.String(required=True, description='Mensaje del evento'),
        'timestamp': fields.String(required=True, description='Timestamp del evento'),
        'source': fields.String(description='Fuente del evento'),
        'details': fields.Raw(description='Detalles adicionales del evento')
    })
    
    # Modelo para métricas del sistema
    system_metrics_model = api.model('SystemMetrics', {
        'cpu_usage': fields.Float(description='Uso de CPU en porcentaje'),
        'memory_usage': fields.Float(description='Uso de memoria en porcentaje'),
        'gpu_usage': fields.Float(description='Uso de GPU en porcentaje'),
        'disk_usage': fields.Float(description='Uso de disco en porcentaje'),
        'active_experiments': fields.Integer(description='Número de experimentos activos'),
        'timestamp': fields.String(required=True, description='Timestamp de las métricas')
    })
    
    # Modelo para estado de conexión
    connection_status_model = api.model('ConnectionStatus', {
        'connected': fields.Boolean(required=True, description='Estado de conexión'),
        'client_id': fields.String(description='ID del cliente'),
        'connected_since': fields.String(description='Timestamp de conexión'),
        'channels': fields.List(fields.String, description='Canales suscritos'),
        'last_heartbeat': fields.String(description='Último heartbeat recibido')
    })
    
    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(description='Código de error'),
        'timestamp': fields.String(description='Timestamp del error')
    })
    
    # Modelo para respuesta exitosa
    success_response_model = api.model('SuccessResponse', {
        'message': fields.String(required=True, description='Mensaje de éxito'),
        'timestamp': fields.String(description='Timestamp de la respuesta')
    })
    
    return {
        'connection_config_model': connection_config_model,
        'training_progress_model': training_progress_model,
        'system_event_model': system_event_model,
        'system_metrics_model': system_metrics_model,
        'connection_status_model': connection_status_model,
        'error_response_model': error_response_model,
        'success_response_model': success_response_model
    }