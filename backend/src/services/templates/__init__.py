# backend/src/services/templates/__init__.py
"""
Servicios de plantillas para arquitecturas ML predefinidas.
"""

from .template_service import TemplateService
from .model_templates import ModelTemplates

__all__ = ['TemplateService', 'ModelTemplates']