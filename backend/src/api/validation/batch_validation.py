# backend/src/api/validation/batch_validation.py
"""
Endpoints especializados para validación en lote refactorizados.

Este módulo contiene únicamente las rutas de validación en lote,
delegando la lógica de negocio al servicio correspondiente.
"""

from flask import Blueprint, request, jsonify
from src.services.validation.batch_validation_service import BatchValidationService

batch_bp = Blueprint('batch_validation', __name__)

# Instancia del servicio de validación en lote
batch_service = BatchValidationService()

@batch_bp.route('/validate', methods=['POST'])
def validate_batch():
    """Valida múltiples configuraciones en lote."""
    try:
        data = request.get_json()
        if not data or 'items' not in data:
            return jsonify({'error': 'No items provided for batch validation'}), 400

        items = data['items']
        if not isinstance(items, list):
            return jsonify({'error': 'Items must be a list'}), 400

        result = batch_service.validate_batch(items)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@batch_bp.route('/health', methods=['GET'])
def batch_health_check():
    """Health check específico para validación en lote."""
    try:
        result = batch_service.health_check()
        status_code = 200 if result['status'] == 'healthy' else 500
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'batch_validation',
            'error': 'Health check failed'
        }), 500