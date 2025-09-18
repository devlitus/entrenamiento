"""
Módulo de API para entrenamiento de modelos.

Exporta las funciones necesarias para crear modelos y namespace de Flask-RESTX.
"""

from .training_models import create_training_models
from .training_routes import create_training_namespace

__all__ = ['create_training_models', 'create_training_namespace']