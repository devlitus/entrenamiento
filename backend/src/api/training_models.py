# backend/src/api/training_models.py
"""
Modelos de datos para endpoints de entrenamiento usando Flask-RESTX.

Define los esquemas de request/response para documentación automática.
"""

from flask_restx import fields

def create_training_models(api):
    """Crea los modelos de datos para training usando la instancia de Api"""
    
    # Modelo para parámetros de entrenamiento
    training_params_model = api.model('TrainingParams', {
        'epochs': fields.Integer(required=True, description='Número de épocas', example=100),
        'batch_size': fields.Integer(required=False, description='Tamaño del batch', example=32),
        'learning_rate': fields.Float(required=False, description='Tasa de aprendizaje', example=0.01),
        'architecture': fields.String(required=False, description='Tipo de arquitectura', example='single_layer'),
        'optimizer': fields.String(required=False, description='Optimizador', example='adam'),
        'loss_function': fields.String(required=False, description='Función de pérdida', example='mse')
    })

    # Modelo para respuesta de inicio de entrenamiento
    training_start_response_model = api.model('TrainingStartResponse', {
        'training_id': fields.String(required=True, description='ID único del entrenamiento'),
        'status': fields.String(required=True, description='Estado del entrenamiento'),
        'message': fields.String(required=True, description='Mensaje descriptivo'),
        'params': fields.Raw(required=True, description='Parámetros utilizados')
    })

    # Modelo para respuesta de estado
    training_status_response_model = api.model('TrainingStatusResponse', {
        'is_training': fields.Boolean(required=True, description='Si está entrenando actualmente'),
        'is_paused': fields.Boolean(required=True, description='Si está pausado'),
        'current_epoch': fields.Integer(required=False, description='Época actual'),
        'total_epochs': fields.Integer(required=False, description='Total de épocas'),
        'current_loss': fields.Float(required=False, description='Pérdida actual'),
        'training_id': fields.String(required=False, description='ID del entrenamiento actual')
    })

    # Modelo para respuesta de control (stop, pause, resume)
    training_control_response_model = api.model('TrainingControlResponse', {
        'status': fields.String(required=True, description='Nuevo estado del entrenamiento'),
        'message': fields.String(required=False, description='Mensaje descriptivo'),
        'timestamp': fields.String(required=False, description='Timestamp de la acción')
    })

    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(required=False, description='Código de error'),
        'details': fields.Raw(required=False, description='Detalles adicionales del error')
    })
    
    return {
        'training_params_model': training_params_model,
        'training_start_response_model': training_start_response_model,
        'training_status_response_model': training_status_response_model,
        'training_control_response_model': training_control_response_model,
        'error_response_model': error_response_model
    }