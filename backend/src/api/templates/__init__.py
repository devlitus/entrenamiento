"""
Módulo de gestión de plantillas de modelos.

Este módulo proporciona funcionalidades para gestionar plantillas de modelos
de machine learning, incluyendo listado, personalización, recomendaciones
y comparación de plantillas.
"""

from .template_models import create_template_models
from .template_routes import create_template_namespace, create_template_blueprint

__all__ = [
    'create_template_models',
    'create_template_namespace', 
    'create_template_blueprint'
]