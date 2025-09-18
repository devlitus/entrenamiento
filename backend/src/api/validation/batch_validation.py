# backend/src/api/validation/batch_validation.py
"""
Endpoints especializados para validación en lote refactorizados.

Este módulo contiene únicamente las rutas de validación en lote,
delegando la lógica de negocio al servicio correspondiente.
"""

from flask import request
from flask_restx import Namespace, Resource
from src.services.validation.batch_validation_service import BatchValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_batch_validation_namespace(models):
    """Crea el namespace de validación en lote con los modelos proporcionados."""
    batch_ns = Namespace('batch', description='Validación en lote de configuraciones')
    
    # Obtener modelos del diccionario
    batch_validation_request_model = models['batch_validation_request_model']
    batch_validation_result_model = models['batch_validation_result_model']
    health_check_model = models['health_check_model']
    error_response_model = models['error_response_model']
    
    # Instancia del servicio de validación en lote
    batch_service = BatchValidationService()

    @batch_ns.route('/validate')
    class BatchValidation(Resource):
        """Validación en lote de configuraciones."""
        
        @batch_ns.expect(batch_validation_request_model)
        @batch_ns.marshal_with(batch_validation_result_model)
        @batch_ns.doc('validate_batch')
        def post(self):
            """Valida múltiples configuraciones en lote."""
            try:
                data = request.get_json()
                if not data or 'items' not in data:
                    return {'error': 'No items provided for batch validation'}, 400

                items = data['items']
                if not isinstance(items, list):
                    return {'error': 'Items must be a list'}, 400

                result = batch_service.validate_batch(items)
                logger.info(f"Validación en lote completada: {len(items)} elementos procesados")
                return result, 200

            except Exception as e:
                logger.error(f"Error en validación en lote: {str(e)}")
                return {'error': 'Internal server error'}, 500

    @batch_ns.route('/health')
    class BatchHealthCheck(Resource):
        """Health check específico para validación en lote."""
        
        @batch_ns.marshal_with(health_check_model)
        @batch_ns.doc('batch_health_check')
        def get(self):
            """Health check específico para validación en lote."""
            try:
                is_healthy = batch_service.health_check()
                
                return {
                    'status': 'healthy' if is_healthy else 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'service': 'batch_validation'
                }, 200 if is_healthy else 503
                
            except Exception as e:
                logger.error(f"Error en health check de batch: {str(e)}")
                return {
                    'status': 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'service': 'batch_validation'
                }, 503

    return batch_ns