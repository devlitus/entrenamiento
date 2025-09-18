# backend/src/schemas/validation_schemas.py

"""
Esquemas de validación para configuraciones del sistema ML.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class LayerType(Enum):
    """Tipos de capas soportadas."""
    DENSE = "dense"
    DROPOUT = "dropout"
    BATCH_NORMALIZATION = "batch_normalization"
    CONV1D = "conv1d"
    CONV2D = "conv2d"
    LSTM = "lstm"
    GRU = "gru"


class ActivationType(Enum):
    """Tipos de activación soportadas."""
    RELU = "relu"
    SIGMOID = "sigmoid"
    TANH = "tanh"
    LINEAR = "linear"
    SOFTMAX = "softmax"
    LEAKY_RELU = "leaky_relu"


class OptimizerType(Enum):
    """Tipos de optimizadores soportados."""
    ADAM = "adam"
    SGD = "sgd"
    RMSPROP = "rmsprop"
    ADAGRAD = "adagrad"


class LossType(Enum):
    """Tipos de funciones de pérdida soportadas."""
    MSE = "mse"
    MAE = "mae"
    BINARY_CROSSENTROPY = "binary_crossentropy"
    CATEGORICAL_CROSSENTROPY = "categorical_crossentropy"
    SPARSE_CATEGORICAL_CROSSENTROPY = "sparse_categorical_crossentropy"


@dataclass
class LayerConfig:
    """Configuración de una capa de red neuronal."""
    type: LayerType
    units: Optional[int] = None
    activation: Optional[ActivationType] = None
    rate: Optional[float] = None  # Para dropout
    filters: Optional[int] = None  # Para capas convolucionales
    kernel_size: Optional[Union[int, tuple]] = None  # Para capas convolucionales
    return_sequences: Optional[bool] = None  # Para capas recurrentes
    
    def validate(self) -> List[str]:
        """Valida la configuración de la capa."""
        errors = []
        
        if self.type == LayerType.DENSE:
            if not self.units or self.units <= 0:
                errors.append("Dense layer must have positive units")
        
        elif self.type == LayerType.DROPOUT:
            if not self.rate or not (0.0 < self.rate < 1.0):
                errors.append("Dropout rate must be between 0 and 1")
        
        elif self.type in [LayerType.CONV1D, LayerType.CONV2D]:
            if not self.filters or self.filters <= 0:
                errors.append("Convolutional layer must have positive filters")
            if not self.kernel_size:
                errors.append("Convolutional layer must have kernel_size")
        
        elif self.type in [LayerType.LSTM, LayerType.GRU]:
            if not self.units or self.units <= 0:
                errors.append("Recurrent layer must have positive units")
        
        return errors


@dataclass
class ArchitectureSchema:
    """Esquema de validación para arquitectura de modelo."""
    layers: List[LayerConfig]
    input_shape: List[int]
    output_shape: Optional[List[int]] = None
    
    def validate(self) -> List[str]:
        """Valida la arquitectura completa."""
        errors = []
        
        # Validar input_shape
        if not self.input_shape or len(self.input_shape) == 0:
            errors.append("input_shape cannot be empty")
        
        if any(dim <= 0 for dim in self.input_shape):
            errors.append("All input_shape dimensions must be positive")
        
        # Validar que hay al menos una capa
        if not self.layers:
            errors.append("Architecture must have at least one layer")
        
        # Validar cada capa
        for i, layer in enumerate(self.layers):
            layer_errors = layer.validate()
            for error in layer_errors:
                errors.append(f"Layer {i}: {error}")
        
        # Validar secuencia lógica de capas
        for i in range(len(self.layers) - 1):
            current_layer = self.layers[i]
            next_layer = self.layers[i + 1]
            
            # Dropout no puede ser seguido por otro dropout
            if (current_layer.type == LayerType.DROPOUT and 
                next_layer.type == LayerType.DROPOUT):
                errors.append(f"Consecutive dropout layers at positions {i} and {i+1}")
        
        return errors


@dataclass
class TrainingParamsSchema:
    """Esquema de validación para parámetros de entrenamiento."""
    epochs: int
    batch_size: int
    learning_rate: float
    optimizer: OptimizerType
    loss: LossType
    validation_split: Optional[float] = 0.2
    shuffle: Optional[bool] = True
    verbose: Optional[int] = 1
    
    def validate(self) -> List[str]:
        """Valida los parámetros de entrenamiento."""
        errors = []
        
        # Validar epochs
        if self.epochs <= 0:
            errors.append("epochs must be positive")
        if self.epochs > 10000:
            errors.append("epochs should not exceed 10000")
        
        # Validar batch_size
        if self.batch_size <= 0:
            errors.append("batch_size must be positive")
        if self.batch_size > 1024:
            errors.append("batch_size should not exceed 1024")
        
        # Validar learning_rate
        if self.learning_rate <= 0:
            errors.append("learning_rate must be positive")
        if self.learning_rate > 1.0:
            errors.append("learning_rate should not exceed 1.0")
        
        # Validar validation_split
        if self.validation_split is not None:
            if not (0.0 <= self.validation_split <= 0.5):
                errors.append("validation_split must be between 0.0 and 0.5")
        
        # Validar verbose
        if self.verbose is not None:
            if self.verbose not in [0, 1, 2]:
                errors.append("verbose must be 0, 1, or 2")
        
        return errors


@dataclass
class DatasetConfigSchema:
    """Esquema de validación para configuración de dataset."""
    name: str
    type: str  # 'synthetic', 'file', 'api'
    source: Optional[Dict[str, Any]] = None
    preprocessing: Optional[Dict[str, Any]] = None
    validation_split: Optional[float] = 0.2
    
    def validate(self) -> List[str]:
        """Valida la configuración del dataset."""
        errors = []
        
        # Validar nombre
        if not self.name or not self.name.strip():
            errors.append("Dataset name cannot be empty")
        
        # Validar tipo
        valid_types = ['synthetic', 'file', 'api']
        if self.type not in valid_types:
            errors.append(f"Dataset type must be one of: {valid_types}")
        
        # Validar source según el tipo
        if self.type == 'file':
            if not self.source or 'path' not in self.source:
                errors.append("File dataset must specify source path")
        
        elif self.type == 'api':
            if not self.source or 'url' not in self.source:
                errors.append("API dataset must specify source URL")
        
        # Validar validation_split
        if self.validation_split is not None:
            if not (0.0 <= self.validation_split <= 0.5):
                errors.append("validation_split must be between 0.0 and 0.5")
        
        return errors


@dataclass
class ExperimentConfigSchema:
    """Esquema de validación para configuración completa de experimento."""
    name: str
    description: str
    architecture: ArchitectureSchema
    training_params: TrainingParamsSchema
    dataset_config: DatasetConfigSchema
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def validate(self) -> List[str]:
        """Valida la configuración completa del experimento."""
        errors = []
        
        # Validar nombre
        if not self.name or not self.name.strip():
            errors.append("Experiment name cannot be empty")
        
        if len(self.name) > 100:
            errors.append("Experiment name should not exceed 100 characters")
        
        # Validar descripción
        if not self.description or not self.description.strip():
            errors.append("Experiment description cannot be empty")
        
        # Validar componentes
        arch_errors = self.architecture.validate()
        for error in arch_errors:
            errors.append(f"Architecture: {error}")
        
        train_errors = self.training_params.validate()
        for error in train_errors:
            errors.append(f"Training params: {error}")
        
        dataset_errors = self.dataset_config.validate()
        for error in dataset_errors:
            errors.append(f"Dataset config: {error}")
        
        # Validar tags
        if self.tags:
            for tag in self.tags:
                if not isinstance(tag, str) or not tag.strip():
                    errors.append("All tags must be non-empty strings")
        
        return errors


# Funciones de utilidad para validación
def validate_architecture_dict(arch_dict: Dict[str, Any]) -> List[str]:
    """Valida un diccionario de arquitectura."""
    try:
        # Convertir capas
        layers = []
        for layer_dict in arch_dict.get('layers', []):
            layer_config = LayerConfig(
                type=LayerType(layer_dict['type']),
                units=layer_dict.get('units'),
                activation=ActivationType(layer_dict['activation']) if layer_dict.get('activation') else None,
                rate=layer_dict.get('rate'),
                filters=layer_dict.get('filters'),
                kernel_size=layer_dict.get('kernel_size'),
                return_sequences=layer_dict.get('return_sequences')
            )
            layers.append(layer_config)
        
        # Crear esquema
        schema = ArchitectureSchema(
            layers=layers,
            input_shape=arch_dict.get('input_shape', []),
            output_shape=arch_dict.get('output_shape')
        )
        
        return schema.validate()
    
    except (KeyError, ValueError, TypeError) as e:
        return [f"Invalid architecture format: {str(e)}"]


def validate_training_params_dict(params_dict: Dict[str, Any]) -> List[str]:
    """Valida un diccionario de parámetros de entrenamiento."""
    try:
        schema = TrainingParamsSchema(
            epochs=params_dict['epochs'],
            batch_size=params_dict['batch_size'],
            learning_rate=params_dict['learning_rate'],
            optimizer=OptimizerType(params_dict['optimizer']),
            loss=LossType(params_dict['loss']),
            validation_split=params_dict.get('validation_split', 0.2),
            shuffle=params_dict.get('shuffle', True),
            verbose=params_dict.get('verbose', 1)
        )
        
        return schema.validate()
    
    except (KeyError, ValueError, TypeError) as e:
        return [f"Invalid training params format: {str(e)}"]


def validate_experiment_config_dict(config_dict: Dict[str, Any]) -> List[str]:
    """Valida un diccionario de configuración de experimento."""
    try:
        # Validar arquitectura
        arch_errors = validate_architecture_dict(config_dict.get('architecture', {}))
        
        # Validar parámetros de entrenamiento
        train_errors = validate_training_params_dict(config_dict.get('training_params', {}))
        
        # Validar dataset
        dataset_dict = config_dict.get('dataset_config', {})
        dataset_schema = DatasetConfigSchema(
            name=dataset_dict.get('name', ''),
            type=dataset_dict.get('type', ''),
            source=dataset_dict.get('source'),
            preprocessing=dataset_dict.get('preprocessing'),
            validation_split=dataset_dict.get('validation_split', 0.2)
        )
        dataset_errors = dataset_schema.validate()
        
        # Combinar errores
        all_errors = []
        for error in arch_errors:
            all_errors.append(f"Architecture: {error}")
        for error in train_errors:
            all_errors.append(f"Training params: {error}")
        for error in dataset_errors:
            all_errors.append(f"Dataset: {error}")
        
        return all_errors
    
    except Exception as e:
        return [f"Invalid experiment config format: {str(e)}"]