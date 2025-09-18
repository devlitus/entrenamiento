# backend/src/api/model_routes.py
"""
Rutas especializadas para operaciones de modelo.

Este módulo contiene todas las rutas relacionadas con validación
y estado de modelos, siguiendo los patrones establecidos.
"""

from flask import Blueprint, jsonify, request
from src.services.validation.model_validation_service import ModelValidationService
from utils.logger import setup_logger

logger = setup_logger()

def create_model_blueprint():
    """Crea un blueprint para rutas de modelo.
    
    Returns:
        Blueprint configurado para modelo
    """
    
    model_bp = Blueprint('model', __name__, url_prefix='/api/model')
    validation_service = ModelValidationService()
    
    @model_bp.route('/architecture/validate', methods=['POST'])
    def validate_architecture():
        """Valida la arquitectura de un modelo."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Validar usando el servicio existente
            result = validation_service.validate_architecture(data)
            
            return jsonify({
                'valid': result.is_valid,
                'errors': result.errors,
                'warnings': result.warnings,
                'suggestions': result.suggestions
            }), 200
            
        except Exception as e:
            logger.error(f"Error validating architecture: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    return model_bp