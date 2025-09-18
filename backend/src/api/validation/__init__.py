# backend/src/api/validation/__init__.py
"""
Módulo de validación refactorizado.

Este módulo organiza los endpoints de validación en namespaces
especializados siguiendo el principio de responsabilidad única
con soporte para Flask-RESTX y documentación automática.
"""

from .architecture_validation import create_architecture_validation_namespace
from .training_validation import create_training_validation_namespace
from .experiment_validation import create_experiment_validation_namespace
from .batch_validation import create_batch_validation_namespace
from .validation_models import create_validation_models

# Exportar funciones de creación de namespaces
__all__ = [
    'create_architecture_validation_namespace', 
    'create_training_validation_namespace', 
    'create_experiment_validation_namespace', 
    'create_batch_validation_namespace',
    'create_validation_models'
]