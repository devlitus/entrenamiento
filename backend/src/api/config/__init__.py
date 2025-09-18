"""
Módulo de configuración avanzada del sistema de entrenamiento.

Este módulo encapsula toda la funcionalidad relacionada con la gestión
de configuraciones del sistema Neural Network Trainer.
"""

from .config_service import ConfigService
from .config_routes import create_config_blueprint

__all__ = ['ConfigService', 'create_config_blueprint']