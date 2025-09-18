# backend/src/api/validation/training_validation.py
"""
Endpoints especializados para validación de parámetros de entrenamiento usando Flask-RESTX.

Este módulo contiene únicamente la lógica de validación de parámetros de entrenamiento,
siguiendo el principio de responsabilidad única.
"""

from flask import request
from flask_restx import Namespace, Resource
from src.services.validation.model_validation_service import ModelValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Instancia del servicio de validación
validation_service = ModelValidationService()

def create_training_validation_namespace(models):
    """Crea el namespace de validación de entrenamiento con los modelos proporcionados."""
    
    training_ns = Namespace('training', description='Validación de parámetros de entrenamiento')
    
    # Obtener modelos del diccionario
    training_params_model = models['training_params_model']
    validation_result_model = models['validation_result_model']
    suggestions_response_model = models['suggestions_response_model']
    health_check_model = models['health_check_model']
    error_response_model = models['error_response_model']

    @training_ns.route('/validate')
    class TrainingValidation(Resource):
        """Validación de parámetros de entrenamiento."""
        
        @training_ns.doc('validate_training_params')
        @training_ns.expect(training_params_model)
        @training_ns.marshal_with(validation_result_model)
        def post(self):
            """Valida los parámetros de entrenamiento.
            
            Verifica que los parámetros proporcionados sean válidos para el entrenamiento
            y retorna errores, advertencias y sugerencias.
            """
            try:
                data = request.get_json()
                if not data:
                    return {'error': 'No data provided'}, 400

                # Validar usando el servicio
                result = validation_service.validate_training_params(data)

                response = {
                    'valid': result.is_valid,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'suggestions': result.suggestions
                }

                return response, 200

            except Exception as e:
                logger.error(f"Error validating training params: {str(e)}")
                return {'error': 'Internal server error'}, 500

    @training_ns.route('/suggestions')
    class TrainingSuggestions(Resource):
        """Sugerencias para parámetros de entrenamiento."""
        
        @training_ns.doc('get_training_suggestions')
        @training_ns.expect(training_params_model)
        @training_ns.marshal_with(suggestions_response_model)
        def post(self):
            """Obtiene sugerencias para mejorar los parámetros de entrenamiento."""
            try:
                data = request.get_json()
                if not data:
                    return {'error': 'No data provided'}, 400

                suggestions = []

                # Sugerencias para entrenamiento
                if 'epochs' in data:
                    epochs = data['epochs']
                    if epochs > 1000:
                        suggestions.append("Considera usar early stopping para entrenamientos largos")
                    elif epochs < 50:
                        suggestions.append("Pocos epochs pueden resultar en underfitting")

                if 'learning_rate' in data:
                    lr = data['learning_rate']
                    if lr > 0.1:
                        suggestions.append("Learning rate alto puede causar inestabilidad")
                    elif lr < 0.001:
                        suggestions.append("Learning rate bajo puede ralentizar convergencia")

                return {'suggestions': suggestions}, 200

            except Exception as e:
                logger.error(f"Error getting training suggestions: {str(e)}")
                return {'error': 'Internal server error'}, 500

    @training_ns.route('/health')
    class TrainingHealthCheck(Resource):
        """Health check para validación de entrenamiento."""
        
        @training_ns.doc('training_health_check')
        @training_ns.marshal_with(health_check_model)
        def get(self):
            """Verifica el estado del servicio de validación de entrenamiento."""
            try:
                # Test básico de validación
                test_config = {
                    'epochs': 100,
                    'learning_rate': 0.001,
                    'batch_size': 32
                }
                
                test_result = validation_service.validate_training_params(test_config)
                
                return {
                    'status': 'healthy',
                    'service': 'training_validation',
                    'test_validation': test_result.is_valid,
                    'timestamp': datetime.now().isoformat()
                }, 200
                
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
                return {
                    'status': 'unhealthy',
                    'service': 'training_validation',
                    'test_validation': False,
                    'timestamp': datetime.now().isoformat()
                }, 500
    
    return training_ns