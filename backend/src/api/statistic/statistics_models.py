# backend/src/api/statistics_models.py
"""Modelos de datos para endpoints de estadísticas usando Flask-RESTX.

Define los esquemas de request/response para documentación automática.
"""

from flask_restx import fields

def create_statistics_models(api):
    """Crea los modelos de datos para statistics usando la instancia de Api"""
    
    # Modelo para respuesta de métricas
    metrics_response_model = api.model('MetricsResponse', {
        'loss': fields.Float(required=True, description='Pérdida actual'),
        'accuracy': fields.Float(required=False, description='Precisión del modelo'),
        'epoch': fields.Integer(required=True, description='Época actual'),
        'training_time': fields.Float(required=False, description='Tiempo de entrenamiento'),
        'validation_loss': fields.Float(required=False, description='Pérdida de validación')
    })

    # Modelo para respuesta de estadísticas del modelo
    model_stats_response_model = api.model('ModelStatsResponse', {
        'total_parameters': fields.Integer(required=True, description='Total de parámetros'),
        'trainable_parameters': fields.Integer(required=True, description='Parámetros entrenables'),
        'model_size_mb': fields.Float(required=False, description='Tamaño del modelo en MB'),
        'architecture': fields.String(required=True, description='Arquitectura del modelo'),
        'last_trained': fields.String(required=False, description='Fecha del último entrenamiento')
    })

    # Modelo para respuesta de historial de entrenamiento
    training_history_response_model = api.model('TrainingHistoryResponse', {
        'epochs': fields.List(fields.Integer, required=True, description='Lista de épocas'),
        'loss_history': fields.List(fields.Float, required=True, description='Historial de pérdidas'),
        'accuracy_history': fields.List(fields.Float, required=False, description='Historial de precisión'),
        'validation_loss_history': fields.List(fields.Float, required=False, description='Historial de pérdida de validación')
    })

    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(required=False, description='Código de error'),
        'details': fields.Raw(required=False, description='Detalles adicionales del error')
    })
    
    return {
        'metrics_response_model': metrics_response_model,
        'model_stats_response_model': model_stats_response_model,
        'training_history_response_model': training_history_response_model,
        'error_response_model': error_response_model
    }