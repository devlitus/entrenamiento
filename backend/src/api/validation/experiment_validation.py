# backend/src/api/validation/experiment_validation.py
"""
Endpoints especializados para validación de configuraciones de experimentos.

Este módulo contiene únicamente la lógica de validación de experimentos
completos, siguiendo el principio de responsabilidad única.
"""

from flask import request
from flask_restx import Namespace, Resource
from src.services.validation.model_validation_service import ModelValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_experiment_validation_namespace(models):
    """Crea el namespace de validación de experimentos con los modelos proporcionados."""
    experiment_ns = Namespace('experiment', description='Validación de configuraciones de experimentos')
    
    # Obtener modelos del diccionario
    experiment_config_model = models['experiment_config_model']
    validation_result_model = models['validation_result_model']
    suggestions_response_model = models['suggestions_response_model']
    health_check_model = models['health_check_model']
    error_response_model = models['error_response_model']
    
    # Instancia del servicio de validación
    validation_service = ModelValidationService()

    @experiment_ns.route('/validate')
    class ExperimentValidation(Resource):
        """Validación de configuraciones de experimentos."""
        
        @experiment_ns.expect(experiment_config_model)
        @experiment_ns.marshal_with(validation_result_model)
        @experiment_ns.doc('validate_experiment_config')
        def post(self):
            """Valida la configuración completa de un experimento.
            
            Returns:
                JSON con resultado de validación y código de estado HTTP
                
            Raises:
                ValidationError: Si la configuración no es válida
            """
            try:
                data = request.get_json()
                if not data:
                    return {'error': 'No data provided'}, 400

                # Validar usando el servicio
                result = validation_service.validate_experiment_config(data)

                response = {
                    'valid': result.is_valid,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'suggestions': result.suggestions
                }

                if result.is_valid:
                    logger.info(f"Configuración de experimento válida: {data.get('name', 'unnamed')}")
                    return response, 200
                else:
                    logger.warning(f"Configuración de experimento inválida: {result.errors}")
                    return response, 400

            except Exception as e:
                logger.error(f"Error validando configuración de experimento: {str(e)}")
                return {
                    'valid': False,
                    'errors': [f'Error interno: {str(e)}'],
                    'warnings': [],
                    'suggestions': []
                }, 500

    @experiment_ns.route('/suggestions')
    class ExperimentSuggestions(Resource):
        """Sugerencias para configuraciones de experimentos."""
        
        @experiment_ns.marshal_with(suggestions_response_model)
        @experiment_ns.doc('get_experiment_suggestions')
        def get(self):
            """Obtiene sugerencias para configuraciones de experimentos."""
            try:
                suggestions = validation_service.get_experiment_suggestions()
                
                return {
                    'suggestions': suggestions,
                    'timestamp': datetime.utcnow().isoformat()
                }, 200
                
            except Exception as e:
                logger.error(f"Error obteniendo sugerencias de experimento: {str(e)}")
                return {
                    'suggestions': [],
                    'timestamp': datetime.utcnow().isoformat()
                }, 500

    @experiment_ns.route('/health')
    class ExperimentHealthCheck(Resource):
        """Health check para validación de experimentos."""
        
        @experiment_ns.marshal_with(health_check_model)
        @experiment_ns.doc('experiment_health_check')
        def get(self):
            """Verifica el estado del servicio de validación de experimentos."""
            try:
                # Verificar que el servicio esté funcionando
                is_healthy = validation_service.health_check()
                
                return {
                    'status': 'healthy' if is_healthy else 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'service': 'experiment_validation'
                }, 200 if is_healthy else 503
                
            except Exception as e:
                logger.error(f"Error en health check de experimento: {str(e)}")
                return {
                    'status': 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'service': 'experiment_validation'
                }, 503

    return experiment_ns