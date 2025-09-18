# backend/src/api/validation/experiment_validation.py
"""
Endpoints especializados para validación de configuraciones de experimentos.

Este módulo contiene únicamente la lógica de validación de experimentos
completos, siguiendo el principio de responsabilidad única.
"""

from flask import Blueprint, request, jsonify
from src.services.validation.model_validation_service import ModelValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
experiment_bp = Blueprint('experiment_validation', __name__)

# Instancia del servicio de validación
validation_service = ModelValidationService()

@experiment_bp.route('/validate', methods=['POST'])
def validate_experiment_config():
    """Valida la configuración completa de un experimento.
    
    Returns:
        JSON con resultado de validación y código de estado HTTP
        
    Raises:
        ValidationError: Si la configuración no es válida
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validar usando el servicio
        result = validation_service.validate_experiment_config(data)

        response = {
            'valid': result.is_valid,
            'errors': result.errors,
            'warnings': result.warnings,
            'suggestions': result.suggestions
        }

        status_code = 200 if result.is_valid else 400
        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error validating experiment config: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@experiment_bp.route('/health', methods=['GET'])
def health_check():
    """Health check para el servicio de validación de configuración de experimentos."""
    try:
        # Test básico de validación
        test_data = {
            'name': 'test_experiment',
            'description': 'Test experiment for health check',
            'architecture': {
                'layers': [64, 32, 1],
                'activation': 'relu',
                'dropout_rate': 0.2
            },
            'training': {
                'epochs': 100,
                'learning_rate': 0.001,
                'batch_size': 32
            }
        }
        
        result = validation_service.validate_experiment_config(test_data)
        
        return jsonify({
            'status': 'healthy',
            'service': 'experiment_validation',
            'test_validation': result.is_valid,
            'timestamp': str(datetime.now())
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'experiment_validation',
            'error': str(e),
            'timestamp': str(datetime.now())
        }), 500

@experiment_bp.route('/suggestions/experiment', methods=['POST'])
def get_experiment_suggestions():
    """Obtiene sugerencias específicas para configuración de experimentos.
    
    Returns:
        JSON con sugerencias específicas para experimentos
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        suggestions = []

        # Sugerencias para experimento completo
        if 'model' in data and 'training' in data:
            model = data['model']
            training = data['training']

            if len(model.get('layers', [])) > 2 and training.get('epochs', 0) < 100:
                suggestions.append("Redes complejas necesitan más epochs para converger")

            if training.get('learning_rate', 0) > 0.1 and len(model.get('layers', [])) > 1:
                suggestions.append("Reduce learning rate para redes multicapa")

        return jsonify({'suggestions': suggestions}), 200

    except Exception as e:
        logger.error(f"Error getting experiment suggestions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@experiment_bp.route('/health/experiment', methods=['GET'])
def experiment_health_check():
    """Health check específico para validación de experimentos.
    
    Returns:
        JSON con estado del servicio de validación de experimentos
    """
    try:
        # Verificar que el servicio funciona con configuración simple
        test_config = {
            'name': 'test_experiment',
            'model': {'layers': [1], 'activation': 'linear'},
            'training': {'epochs': 100, 'learning_rate': 0.01}
        }
        result = validation_service.validate_experiment_config(test_config)

        return jsonify({
            'status': 'healthy',
            'service': 'experiment_validation',
            'test_validation': result.is_valid,
            'timestamp': '2024-01-15T10:30:00Z'
        }), 200

    except Exception as e:
        logger.error(f"Experiment health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'experiment_validation',
            'error': str(e),
            'timestamp': '2024-01-15T10:30:00Z'
        }), 500