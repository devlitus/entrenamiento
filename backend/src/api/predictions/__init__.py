"""
Módulo de predicciones refactorizado.

Proporciona funcionalidades de predicción modularizadas con
soporte para Flask-RESTX y documentación automática.
"""

# Importar desde el archivo de prediction_routes en el directorio predictions
from .prediction_routes import create_prediction_blueprint, create_prediction_namespace
from .prediction_models import create_prediction_models

__all__ = ['create_prediction_blueprint', 'create_prediction_namespace', 'create_prediction_models']