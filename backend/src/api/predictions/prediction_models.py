# backend/src/api/prediction_models.py
"""
Modelos de datos para endpoints de predicción usando Flask-RESTX.

Define los esquemas de request/response para documentación automática.
"""

from flask_restx import fields

def create_prediction_models(api):
    """Crea los modelos de datos para prediction usando la instancia de Api"""
    
    # Modelo para parámetros de predicción
    prediction_params_model = api.model('PredictionParams', {
        'input_data': fields.List(fields.Float, required=True, description='Datos de entrada para predicción'),
        'model_type': fields.String(required=False, description='Tipo de modelo a usar', example='single_layer'),
        'normalize': fields.Boolean(required=False, description='Si normalizar los datos', example=True)
    })

    # Modelo para respuesta de predicción
    prediction_response_model = api.model('PredictionResponse', {
        'prediction': fields.List(fields.Float, required=True, description='Resultado de la predicción'),
        'confidence': fields.Float(required=False, description='Nivel de confianza'),
        'model_used': fields.String(required=True, description='Modelo utilizado'),
        'processing_time': fields.Float(required=False, description='Tiempo de procesamiento en segundos')
    })

    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(required=False, description='Código de error'),
        'details': fields.Raw(required=False, description='Detalles adicionales del error')
    })
    
    return {
        'prediction_params_model': prediction_params_model,
        'prediction_response_model': prediction_response_model,
        'error_response_model': error_response_model
    }