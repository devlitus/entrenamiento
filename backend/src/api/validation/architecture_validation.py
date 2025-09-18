# backend/src/api/validation/architecture_validation.py
"""
Endpoints especializados para validación de arquitecturas de modelos.

Este módulo contiene únicamente la lógica de validación de arquitecturas,
siguiendo el principio de responsabilidad única.
"""

from flask import Blueprint, request, jsonify
from src.services.validation.model_validation_service import ModelValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
architecture_bp = Blueprint('architecture_validation', __name__)

# Instancia del servicio de validación
validation_service = ModelValidationService()

@architecture_bp.route('/validate', methods=['POST'])
def validate_architecture():
    """Valida la arquitectura de un modelo.
    
    Returns:
        JSON con resultado de validación y código de estado HTTP
        
    Raises:
        ValidationError: Si los parámetros no son válidos
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validar usando el servicio
        result = validation_service.validate_architecture(data)

        response = {
            'valid': result.is_valid,
            'errors': result.errors,
            'warnings': result.warnings,
            'suggestions': result.suggestions
        }

        status_code = 200 if result.is_valid else 400
        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error validating architecture: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@architecture_bp.route('/health', methods=['GET'])
def health_check():
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
        
        return jsonify({
            'status': 'healthy',
            'service': 'architecture_validation',
            'test_validation': result.is_valid,
            'timestamp': str(datetime.now())
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'architecture_validation',
            'error': str(e),
            'timestamp': str(datetime.now())
        }), 500

@architecture_bp.route('/suggestions/architecture', methods=['POST'])
def get_architecture_suggestions():
    """Obtiene sugerencias específicas para arquitectura de modelo.
    
    Returns:
        JSON con sugerencias específicas para la arquitectura
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

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

        return jsonify({'suggestions': suggestions}), 200

    except Exception as e:
        logger.error(f"Error getting architecture suggestions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@architecture_bp.route('/health/architecture', methods=['GET'])
def architecture_health_check():
    """Health check específico para validación de arquitecturas.
    
    Returns:
        JSON con estado del servicio de validación de arquitecturas
    """
    try:
        # Verificar que el servicio funciona con una validación simple
        test_config = {'layers': [1], 'activation': 'linear'}
        result = validation_service.validate_architecture(test_config)

        return jsonify({
            'status': 'healthy',
            'service': 'architecture_validation',
            'test_validation': result.is_valid,
            'timestamp': '2024-01-15T10:30:00Z'
        }), 200

    except Exception as e:
        logger.error(f"Architecture health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'architecture_validation',
            'error': str(e),
            'timestamp': '2024-01-15T10:30:00Z'
        }), 500