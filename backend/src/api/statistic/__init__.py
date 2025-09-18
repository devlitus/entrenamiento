"""
Módulo de estadísticas y métricas.

Proporciona funcionalidades de estadísticas y métricas con
soporte para Flask-RESTX y documentación automática.
"""

from .statistics_routes import create_statistics_namespace, create_statistics_blueprint
from .statistics_models import create_statistics_models

__all__ = ['create_statistics_namespace', 'create_statistics_blueprint', 'create_statistics_models']