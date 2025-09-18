# backend/src/api/validation/__init__.py
"""
Módulo de validación refactorizado.

Este módulo organiza los endpoints de validación en sub-blueprints
especializados siguiendo el principio de responsabilidad única.
"""

from flask import Blueprint
from .architecture_validation import architecture_bp
from .training_validation import training_bp
from .experiment_validation import experiment_bp
from .batch_validation import batch_bp

# Blueprint principal de validación
validation_bp = Blueprint('validation', __name__, url_prefix='/api/validation')

# Registrar sub-blueprints
validation_bp.register_blueprint(architecture_bp, url_prefix='/architecture')
validation_bp.register_blueprint(training_bp, url_prefix='/training')
validation_bp.register_blueprint(experiment_bp, url_prefix='/experiment')
validation_bp.register_blueprint(batch_bp, url_prefix='/batch')

# Exportar blueprint principal
__all__ = ['validation_bp']