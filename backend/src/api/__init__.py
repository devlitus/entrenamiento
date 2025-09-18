# backend/src/api/__init__.py
"""
API module initialization.

Imports and exposes all blueprints from the API modules.
"""

from .config import create_config_blueprint
from .experiments import create_experiment_blueprint
from .templates import create_template_blueprint
from .predictions import create_prediction_blueprint

__all__ = [
    'create_config_blueprint',
    'create_experiment_blueprint', 
    'create_template_blueprint',
    'create_prediction_blueprint'
]