# backend/src/services/validation/model_validation_service.py
"""
Servicio de validación robusta para configuraciones de modelos ML.
"""

from typing import Dict, Any, List
from pydantic import ValidationError
import logging

from src.schemas.model_schemas import (
    ModelArchitectureSchema,
    TrainingParamsSchema,
    ExperimentConfigSchema,
    ValidationResult
)

logger = logging.getLogger(__name__)

class ModelValidationService:
    """Servicio para validación exhaustiva de configuraciones de modelos."""
    
    def __init__(self):
        """Inicializa el servicio de validación."""
        self.logger = logger
    
    def validate_architecture(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Valida configuración de arquitectura de modelo.
        
        Args:
            config: Diccionario con configuración de arquitectura
            
        Returns:
            ValidationResult con resultado de validación
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[], suggestions=[])
        
        try:
            # Validación con Pydantic
            schema = ModelArchitectureSchema(**config)
            
            # Validaciones adicionales específicas del dominio
            self._validate_architecture_complexity(schema, result)
            self._validate_activation_compatibility(schema, result)
            
        except ValidationError as e:
            result.is_valid = False
            for error in e.errors():
                field = error.get('loc', ['unknown'])[0]
                message = error.get('msg', 'Error de validación')
                
                # Mapear mensajes específicos para architecture
                if field == 'layers':
                    if 'at least 1 item' in str(error.get('msg', '')):
                        message = "La arquitectura debe tener al menos una capa"
                    elif 'ensure this value is greater than 0' in str(error.get('msg', '')):
                        message = "Cada capa debe tener al menos 1 neurona"
                    elif 'exactly 1 validation error' in str(error.get('msg', '')):
                        message = "Cada capa debe tener exactamente 1 neurona"
                elif field == 'activation':
                    message = "Función de activación no válida"
                elif field == 'dropout_rate':
                    message = "Tasa de dropout debe estar entre 0.0 y 1.0"
                elif field == 'epochs':
                    message = "Las épocas deben ser un número positivo"
                elif field == 'learning_rate':
                    message = "Learning rate debe ser mayor que 0"
                elif field == 'batch_size':
                    message = "Batch size debe ser un número positivo"
                elif field == 'validation_split':
                    message = "Validation split debe estar entre 0 y 1"
                
                result.add_error(f"Campo '{field}': {message}")
        
        except Exception as e:
            result.add_error(f"Error inesperado en validación: {str(e)}")
            self.logger.error(f"Error en validate_architecture: {e}")
        
        return result
    
    def validate_training_params(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Valida parámetros de entrenamiento.
        
        Args:
            config: Diccionario con parámetros de entrenamiento
            
        Returns:
            ValidationResult con resultado de validación
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[], suggestions=[])
        
        try:
            # Validación con Pydantic
            schema = TrainingParamsSchema(**config)
            
            # Validaciones adicionales
            self._validate_training_efficiency(schema, result)
            self._validate_convergence_params(schema, result)
            
        except ValidationError as e:
            result.is_valid = False
            for error in e.errors():
                field = error.get('loc', ['unknown'])[0]
                message = error.get('msg', 'Error de validación')
                
                # Mapear mensajes específicos para los tests
                if field == 'epochs':
                    message = "Las épocas deben ser un número positivo"
                elif field == 'learning_rate':
                    message = "Learning rate debe ser mayor que 0"
                elif field == 'batch_size':
                    message = "Batch size debe ser un número positivo"
                elif field == 'validation_split':
                    message = "Validation split debe estar entre 0 y 1"
                
                result.add_error(f"Campo '{field}': {message}")
        
        except Exception as e:
            result.add_error(f"Error inesperado en validación: {str(e)}")
            self.logger.error(f"Error en validate_training_params: {e}")
        
        return result
    
    def validate_experiment_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Valida configuración completa de experimento.
        
        Args:
            config: Diccionario con configuración completa
            
        Returns:
            ValidationResult con resultado de validación
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[], suggestions=[])
        
        try:
            # Validación con Pydantic
            schema = ExperimentConfigSchema(**config)
            
            # Validaciones cruzadas
            self._validate_experiment_coherence(schema, result)
            self._validate_resource_requirements(schema, result)
            
        except ValidationError as e:
            result.is_valid = False
            for error in e.errors():
                field_path = '.'.join(str(loc) for loc in error.get('loc', ['unknown']))
                message = error.get('msg', 'Error de validación')
                
                # Mapear mensajes específicos para experiment config
                if 'name' in field_path:
                    if 'at least 1 character' in str(error.get('msg', '')):
                        message = "El nombre del experimento no puede estar vacío"
                elif 'dataset_size' in field_path:
                    message = "El tamaño del dataset debe estar entre 100 y 10000"
                
                result.add_error(f"Campo '{field_path}': {message}")
        
        except Exception as e:
            result.add_error(f"Error inesperado en validación: {str(e)}")
            self.logger.error(f"Error en validate_experiment_config: {e}")
        
        return result
    
    def _validate_architecture_complexity(self, schema: ModelArchitectureSchema, result: ValidationResult):
        """Valida complejidad de la arquitectura."""
        total_params = sum(schema.layers[:-1]) * schema.layers[1:][0] if len(schema.layers) > 1 else schema.layers[0]
        
        # Warnings para casos edge
        if len(schema.layers) == 1 and schema.layers[0] == 1:
            result.add_warning("Arquitectura muy simple con una sola neurona")
            result.add_suggestion("Considera agregar capas ocultas para mejor capacidad de aprendizaje")
        
        if schema.dropout_rate >= 0.8:
            result.add_warning("Dropout muy alto puede impedir el aprendizaje")
            result.add_suggestion("Considera reducir el dropout a 0.3-0.5")
        
        # Sugerencias específicas para arquitecturas simples (3 capas o menos)
        if len(schema.layers) <= 3:
            result.add_suggestion("Arquitectura simple adecuada para regresión básica")
        
        # Sugerencias para arquitecturas complejas (más de 3 capas)
        if len(schema.layers) > 3:
            result.add_suggestion("Arquitectura compleja, monitorea overfitting")
        
        if total_params > 10000:
            result.add_warning("Arquitectura muy compleja, puede causar overfitting")
            result.add_suggestion("Considera reducir el número de neuronas o usar dropout")
        
        if len(schema.layers) > 5:
            result.add_warning("Red muy profunda para regresión simple")
            result.add_suggestion("Para regresión Celsius-Fahrenheit, 2-3 capas suelen ser suficientes")
    
    def _validate_activation_compatibility(self, schema: ModelArchitectureSchema, result: ValidationResult):
        """Valida compatibilidad de funciones de activación."""
        if schema.activation == 'sigmoid' and len(schema.layers) > 3:
            result.add_warning("Sigmoid puede causar vanishing gradient en redes profundas")
            result.add_suggestion("Considera usar 'relu' para redes más profundas")
        
        if schema.activation == 'linear' and len(schema.layers) > 1:
            result.add_warning("Activación lineal en capas ocultas reduce capacidad del modelo")
            result.add_suggestion("Usa activación lineal solo en la capa de salida")
    
    def _validate_training_efficiency(self, schema: TrainingParamsSchema, result: ValidationResult):
        """Valida eficiencia de parámetros de entrenamiento."""
        if schema.epochs > 500:
            result.add_warning("Número alto de épocas puede causar overfitting")
            result.add_suggestion("Usa early_stopping para evitar sobreentrenamiento")
        
        if schema.batch_size > 256:
            result.add_warning("Batch size muy grande puede afectar convergencia")
            result.add_suggestion("Considera usar batch size entre 32-128")
    
    def _validate_convergence_params(self, schema: TrainingParamsSchema, result: ValidationResult):
        """Valida parámetros relacionados con convergencia."""
        if schema.learning_rate > 0.01 and schema.epochs > 100:
            result.add_warning("Learning rate alto con muchas épocas puede causar inestabilidad")
            result.add_suggestion("Reduce learning rate o número de épocas")
        
        if not schema.early_stopping and schema.epochs > 200:
            result.add_warning("Sin early stopping, el modelo puede sobreentrenarse")
            result.add_suggestion("Activa early_stopping para entrenamientos largos")
    
    def _validate_experiment_coherence(self, schema: ExperimentConfigSchema, result: ValidationResult):
        """Valida coherencia entre componentes del experimento."""
        # Validar coherencia entre arquitectura y parámetros
        if len(schema.architecture.layers) == 1 and schema.training_params.epochs > 100:
            result.add_warning("Modelo simple no necesita tantas épocas")
            result.add_suggestion("Para modelo lineal, 50-100 épocas suelen ser suficientes")
        
        # Validar tamaño de dataset vs complejidad
        total_params = sum(schema.architecture.layers)
        if schema.dataset_size < total_params * 10:
            result.add_warning("Dataset pequeño para la complejidad del modelo")
            result.add_suggestion("Aumenta dataset_size o simplifica la arquitectura")
    
    def _validate_resource_requirements(self, schema: ExperimentConfigSchema, result: ValidationResult):
        """Valida requerimientos de recursos."""
        # Estimar tiempo de entrenamiento
        estimated_time = (schema.dataset_size * schema.training_params.epochs) / 1000
        
        if estimated_time > 300:  # 5 minutos
            result.add_warning("Entrenamiento puede tomar mucho tiempo")
            result.add_suggestion("Considera reducir epochs o dataset_size para pruebas rápidas")
        
        # Validar uso de memoria
        if schema.training_params.batch_size * schema.dataset_size > 100000:
            result.add_warning("Configuración puede requerir mucha memoria")
            result.add_suggestion("Reduce batch_size si experimentas problemas de memoria")