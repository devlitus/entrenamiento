# backend/src/schemas/__init__.py

"""
Schemas package for Neural Network Trainer

This package contains data validation schemas and models used throughout the application.
"""

# Import validation schemas
from .validation_schemas import (
    ArchitectureSchema,
    TrainingParamsSchema,
    ExperimentConfigSchema,
    DatasetConfigSchema
)

# Import response models
from .response_models import (
    ValidationResult,
    ExperimentResponse,
    RunResponse,
    TemplateResponse,
    ComparisonResponse
)

__all__ = [
    # Validation schemas
    'ArchitectureSchema',
    'TrainingParamsSchema', 
    'ExperimentConfigSchema',
    'DatasetConfigSchema',
    
    # Response models
    'ValidationResult',
    'ExperimentResponse',
    'RunResponse',
    'TemplateResponse',
    'ComparisonResponse'
]
"""
Esquemas de validación para el sistema de entrenamiento ML.
"""

from .model_schemas import (
    ModelArchitectureSchema,
    TrainingParamsSchema,
    ExperimentConfigSchema,
    ValidationResult
)

__all__ = [
    'ModelArchitectureSchema',
    'TrainingParamsSchema', 
    'ExperimentConfigSchema',
    'ValidationResult'
]