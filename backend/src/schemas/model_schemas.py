# backend/src/schemas/model_schemas.py
"""
Esquemas Pydantic para validación estricta de configuraciones de modelos.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from dataclasses import dataclass
from datetime import datetime

class ModelArchitectureSchema(BaseModel):
    """Esquema para validación de arquitectura de modelo."""
    
    layers: List[int] = Field(..., min_length=1, max_length=10, description="Número de neuronas por capa")
    activation: str = Field(..., pattern="^(relu|sigmoid|tanh|linear|swish)$", description="Función de activación")
    dropout_rate: float = Field(0.0, ge=0.0, le=0.9, description="Tasa de dropout")
    batch_normalization: bool = Field(False, description="Usar normalización por lotes")
    
    @field_validator('layers')
    @classmethod
    def validate_layers(cls, v):
        """Valida que las capas tengan valores positivos."""
        if any(layer <= 0 for layer in v):
            raise ValueError("Todas las capas deben tener al menos 1 neurona")
        return v
    
    @field_validator('layers')
    @classmethod
    def validate_output_layer(cls, v):
        """Valida que la última capa sea apropiada para regresión."""
        if v[-1] != 1:
            raise ValueError("La capa de salida debe tener exactamente 1 neurona para regresión")
        return v

class TrainingParamsSchema(BaseModel):
    """Esquema para validación de parámetros de entrenamiento."""
    
    epochs: int = Field(..., ge=1, le=1000, description="Número de épocas")
    learning_rate: float = Field(..., gt=0.0, le=1.0, description="Tasa de aprendizaje")
    batch_size: int = Field(32, ge=1, le=512, description="Tamaño del lote")
    validation_split: float = Field(0.2, ge=0.1, le=0.5, description="Proporción de datos para validación")
    early_stopping: bool = Field(True, description="Usar parada temprana")
    patience: int = Field(10, ge=1, le=50, description="Paciencia para parada temprana")
    
    @field_validator('epochs')
    @classmethod
    def validate_epochs(cls, v):
        """Valida que las épocas sean válidas."""
        if v <= 0:
            raise ValueError("Las épocas deben ser un número positivo")
        return v
    
    @field_validator('learning_rate')
    @classmethod
    def validate_learning_rate(cls, v):
        """Valida que la tasa de aprendizaje esté en un rango razonable."""
        if v <= 0:
            raise ValueError("Learning rate debe ser mayor que 0")
        if v < 0.0001 or v > 0.1:
            raise ValueError("Tasa de aprendizaje debe estar entre 0.0001 y 0.1")
        return v
    
    @field_validator('batch_size')
    @classmethod
    def validate_batch_size(cls, v):
        """Valida que el batch size sea válido."""
        if v <= 0:
            raise ValueError("Batch size debe ser un número positivo")
        return v
    
    @field_validator('validation_split')
    @classmethod
    def validate_validation_split(cls, v):
        """Valida que el validation split esté en rango válido."""
        if v <= 0 or v >= 1:
            raise ValueError("Validation split debe estar entre 0 y 1")
        return v

class ExperimentConfigSchema(BaseModel):
    """Esquema para configuración completa de experimento."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del experimento")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del experimento")
    architecture: ModelArchitectureSchema = Field(..., description="Configuración de arquitectura")
    training_params: TrainingParamsSchema = Field(..., description="Parámetros de entrenamiento")
    dataset_size: int = Field(1000, ge=100, le=10000, description="Tamaño del dataset")
    tags: List[str] = Field(default_factory=list, description="Etiquetas del experimento")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Valida que el nombre sea alfanumérico con guiones."""
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("El nombre solo puede contener letras, números, guiones y guiones bajos")
        return v

@dataclass
class ValidationResult:
    """Resultado de validación de configuración."""
    
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    
    def __post_init__(self):
        """Inicializa listas vacías si son None."""
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.suggestions is None:
            self.suggestions = []
    
    def add_error(self, error: str):
        """Agrega un error y marca como inválido."""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """Agrega una advertencia."""
        self.warnings.append(warning)
    
    def add_suggestion(self, suggestion: str):
        """Agrega una sugerencia."""
        self.suggestions.append(suggestion)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para serialización."""
        return {
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }