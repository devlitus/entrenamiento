# backend/src/api/validation/architecture_validation.py
"""
Endpoints especializados para validación de arquitecturas de modelos usando Flask-RESTX.

Este módulo contiene únicamente la lógica de validación de arquitecturas,
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

def create_architecture_validation_namespace(models):
    """Crea el namespace de validación de arquitecturas con los modelos proporcionados."""
    
    architecture_ns = Namespace('architecture', description='Validación de arquitecturas de modelos')
    
    # Obtener modelos
    architecture_config_model = models['architecture_config_model']
    validation_result_model = models['validation_result_model']
    suggestions_response_model = models['suggestions_response_model']
    health_check_model = models['health_check_model']
    error_response_model = models['error_response_model']

    @architecture_ns.route('/validate')
    class ArchitectureValidation(Resource):
        @architecture_ns.expect(architecture_config_model)
        @architecture_ns.marshal_with(validation_result_model, code=200, description='Validación exitosa')
        @architecture_ns.marshal_with(error_response_model, code=400, description='Error de validación')
        @architecture_ns.marshal_with(error_response_model, code=500, description='Error interno del servidor')
        def post(self):
            """Valida la arquitectura de un modelo."""
            try:
                data = request.get_json()
                if not data:
                    return {'error': 'No data provided'}, 400

                # Validar usando el servicio
                result = validation_service.validate_architecture(data)

                response = {
                    'valid': result.is_valid,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'suggestions': result.suggestions
                }

                status_code = 200 if result.is_valid else 400
                return response, status_code

            except Exception as e:
                logger.error(f"Error validating architecture: {str(e)}")
                return {'error': 'Internal server error'}, 500

    @architecture_ns.route('/health')
    class ArchitectureHealth(Resource):
        @architecture_ns.marshal_with(health_check_model, code=200, description='Servicio saludable')
        @architecture_ns.marshal_with(error_response_model, code=500, description='Servicio no saludable')
        def get(self):
            """Health check para el servicio de validación de arquitecturas."""
            try:
                # Test básico de validación
                test_data = {
                    'layers': [64, 32, 1],
                    'activation': 'relu',
                    'dropout_rate': 0.2,
                    'batch_normalization': False
                }
                
                result = validation_service.validate_architecture(test_data)
                
                return {
                    'status': 'healthy',
                    'service': 'architecture_validation',
                    'test_validation': result.is_valid,
                    'timestamp': str(datetime.now())
                }, 200
                
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
                return {
                    'status': 'unhealthy',
                    'service': 'architecture_validation',
                    'error': str(e),
                    'timestamp': str(datetime.now())
                }, 500

    @architecture_ns.route('/suggestions')
    class ArchitectureSuggestions(Resource):
        @architecture_ns.expect(architecture_config_model)
        @architecture_ns.marshal_with(suggestions_response_model, code=200, description='Sugerencias obtenidas')
        @architecture_ns.marshal_with(error_response_model, code=400, description='Error en la solicitud')
        @architecture_ns.marshal_with(error_response_model, code=500, description='Error interno del servidor')
        def post(self):
            """Obtiene sugerencias específicas para arquitectura de modelo."""
            try:
                data = request.get_json()
                if not data:
                    return {'error': 'No data provided'}, 400

                suggestions = []

                # Sugerencias para arquitectura
                if 'layers' in data:
                    layers = data['layers']
                    if len(layers) == 1 and layers[0] == 1:
                        suggestions.append("Para regresión simple, considera usar activación 'linear'")
                    elif len(layers) > 1:
                        suggestions.append("Para redes multicapa, considera usar 'relu' en capas ocultas")
                    if 'dropout_rate' not in data:
                        suggestions.append("Considera agregar dropout para prevenir overfitting")

                return {'suggestions': suggestions}, 200

            except Exception as e:
                logger.error(f"Error getting architecture suggestions: {str(e)}")
                return {'error': 'Internal server error'}, 500

    return architecture_ns