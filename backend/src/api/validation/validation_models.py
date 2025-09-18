# backend/src/api/validation/validation_models.py
"""
Modelos de datos para endpoints de validación usando Flask-RESTX.

Define los esquemas de request/response para documentación automática
de todos los endpoints de validación.
"""

from flask_restx import fields

def create_validation_models(api):
    """Crea y retorna todos los modelos de validación para Flask-RESTX."""
    
    # Modelo base para resultado de validación
    validation_result_model = api.model('ValidationResult', {
        'valid': fields.Boolean(required=True, description='Si la validación es exitosa'),
        'errors': fields.List(fields.String, required=True, description='Lista de errores encontrados'),
        'warnings': fields.List(fields.String, required=True, description='Lista de advertencias'),
        'suggestions': fields.List(fields.String, required=True, description='Lista de sugerencias de mejora')
    })
    
    # Modelo para configuración de arquitectura
    architecture_config_model = api.model('ArchitectureConfig', {
        'layers': fields.List(fields.Integer, required=True, description='Configuración de capas', example=[64, 32, 1]),
        'activation': fields.String(required=True, description='Función de activación', example='relu'),
        'dropout_rate': fields.Float(required=False, description='Tasa de dropout', example=0.2),
        'batch_normalization': fields.Boolean(required=False, description='Usar normalización por lotes', example=False)
    })
    
    # Modelo para parámetros de entrenamiento
    training_params_model = api.model('TrainingParams', {
        'epochs': fields.Integer(required=True, description='Número de épocas', example=100),
        'learning_rate': fields.Float(required=True, description='Tasa de aprendizaje', example=0.001),
        'batch_size': fields.Integer(required=True, description='Tamaño del lote', example=32),
        'early_stopping': fields.Boolean(required=False, description='Usar parada temprana', example=True),
        'patience': fields.Integer(required=False, description='Paciencia para parada temprana', example=10),
        'validation_split': fields.Float(required=False, description='División de validación', example=0.2)
    })
    
    # Modelo para configuración de experimento
    experiment_config_model = api.model('ExperimentConfig', {
        'name': fields.String(required=True, description='Nombre del experimento'),
        'description': fields.String(required=False, description='Descripción del experimento'),
        'architecture': fields.Nested(architecture_config_model, required=True, description='Configuración de arquitectura'),
        'training_params': fields.Nested(training_params_model, required=True, description='Parámetros de entrenamiento'),
        'data_config': fields.Raw(required=False, description='Configuración de datos')
    })
    
    # Modelo para validación en lote
    batch_validation_request_model = api.model('BatchValidationRequest', {
        'items': fields.List(fields.Raw, required=True, description='Lista de configuraciones a validar')
    })
    
    # Modelo para resultado de validación en lote
    batch_validation_result_model = api.model('BatchValidationResult', {
        'total_items': fields.Integer(required=True, description='Total de elementos validados'),
        'valid_items': fields.Integer(required=True, description='Elementos válidos'),
        'invalid_items': fields.Integer(required=True, description='Elementos inválidos'),
        'results': fields.List(fields.Nested(validation_result_model), required=True, description='Resultados individuales')
    })
    
    # Modelo para sugerencias
    suggestions_response_model = api.model('SuggestionsResponse', {
        'suggestions': fields.List(fields.String, required=True, description='Lista de sugerencias')
    })
    
    # Modelo para health check
    health_check_model = api.model('HealthCheck', {
        'status': fields.String(required=True, description='Estado del servicio', example='healthy'),
        'service': fields.String(required=True, description='Nombre del servicio'),
        'test_validation': fields.Boolean(required=False, description='Resultado de validación de prueba'),
        'timestamp': fields.String(required=True, description='Timestamp del check')
    })
    
    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(required=False, description='Código de error'),
        'details': fields.Raw(required=False, description='Detalles adicionales del error')
    })
    
    return {
        'validation_result_model': validation_result_model,
        'architecture_config_model': architecture_config_model,
        'training_params_model': training_params_model,
        'experiment_config_model': experiment_config_model,
        'batch_validation_request_model': batch_validation_request_model,
        'batch_validation_result_model': batch_validation_result_model,
        'suggestions_response_model': suggestions_response_model,
        'health_check_model': health_check_model,
        'error_response_model': error_response_model
    }