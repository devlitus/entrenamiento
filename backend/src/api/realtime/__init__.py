"""
Módulo de comunicación en tiempo real.

Proporciona funcionalidades de Server-Sent Events y comunicación
en tiempo real con soporte para Flask-RESTX y documentación automática.
"""

from .realtime_routes import create_realtime_namespace
from .realtime_models import create_realtime_models

__all__ = ['create_realtime_namespace', 'create_realtime_models']