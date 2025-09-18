"""
Módulo de dashboard para métricas y estadísticas del sistema.

Este módulo proporciona endpoints y modelos para el dashboard
de monitoreo del sistema de entrenamiento de redes neuronales.
"""

from .dashboard_models import create_dashboard_models
from .dashboard_routes import create_dashboard_namespace

__all__ = [
    'create_dashboard_models',
    'create_dashboard_namespace'
]