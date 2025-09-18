# backend/src/api/validation/training_validation.py
"""
Endpoints especializados para validación de parámetros de entrenamiento.

Este módulo contiene únicamente la lógica de validación de parámetros
de entrenamiento, siguiendo el principio de responsabilidad única.
"""

from flask import Blueprint, request, jsonify
from src.services.validation.model_validation_service import ModelValidationService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
training_bp = Blueprint('training_validation', __name__)

# Instancia del servicio de validación
validation_service = ModelValidationService()

@training_bp.route('/validate', methods=['POST'])
def validate_training_params():
    """Valida los parámetros de entrenamiento.
    
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
        result = validation_service.validate_training_params(data)

        response = {
            'valid': result.is_valid,
            'errors': result.errors,
            'warnings': result.warnings,
            'suggestions': result.suggestions
        }

        status_code = 200 if result.is_valid else 400
        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error validating training params: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@training_bp.route('/health', methods=['GET'])
def health_check():
    """Health check para el servicio de validación de parámetros de entrenamiento."""
    try:
        # Test básico de validación
        test_data = {
            'epochs': 100,
            'learning_rate': 0.001,
            'batch_size': 32,
            'early_stopping': True,
            'patience': 10,
            'validation_split': 0.2
        }
        
        result = validation_service.validate_training_params(test_data)
        
        return jsonify({
            'status': 'healthy',
            'service': 'training_validation',
            'test_validation': result.is_valid,
            'timestamp': str(datetime.now())
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'training_validation',
            'error': str(e),
            'timestamp': str(datetime.now())
        }), 500

@training_bp.route('/suggestions/training', methods=['POST'])
def get_training_suggestions():
    """Obtiene sugerencias específicas para parámetros de entrenamiento.
    
    Returns:
        JSON con sugerencias específicas para entrenamiento
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

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

        return jsonify({'suggestions': suggestions}), 200

    except Exception as e:
        logger.error(f"Error getting training suggestions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@training_bp.route('/health/training', methods=['GET'])
def training_health_check():
    """Health check específico para validación de parámetros de entrenamiento.
    
    Returns:
        JSON con estado del servicio de validación de entrenamiento
    """
    try:
        # Verificar que el servicio funciona con parámetros simples
        test_params = {'epochs': 100, 'learning_rate': 0.01}
        result = validation_service.validate_training_params(test_params)

        return jsonify({
            'status': 'healthy',
            'service': 'training_validation',
            'test_validation': result.is_valid,
            'timestamp': '2024-01-15T10:30:00Z'
        }), 200

    except Exception as e:
        logger.error(f"Training health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'training_validation',
            'error': str(e),
            'timestamp': '2024-01-15T10:30:00Z'
        }), 500