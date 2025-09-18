# backend/src/services/templates/model_templates.py
"""
Plantillas predefinidas para arquitecturas de modelos ML comunes.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ModelTemplate:
    """Plantilla de modelo con configuración predefinida."""
    
    name: str
    description: str
    architecture: Dict[str, Any]
    training_params: Dict[str, Any]
    use_cases: List[str]
    complexity: str  # 'simple', 'medium', 'complex'
    estimated_training_time: str

class ModelTemplates:
    """Colección de plantillas predefinidas para modelos ML."""
    
    @staticmethod
    def get_simple_regression() -> ModelTemplate:
        """Plantilla para regresión lineal simple."""
        return ModelTemplate(
            name="simple_regression",
            description="Modelo lineal simple para regresión básica Celsius-Fahrenheit",
            architecture={
                "layers": [1],
                "activation": "linear",
                "dropout_rate": 0.0,
                "batch_normalization": False
            },
            training_params={
                "epochs": 100,
                "learning_rate": 0.01,
                "batch_size": 32,
                "validation_split": 0.2,
                "early_stopping": True,
                "patience": 10
            },
            use_cases=[
                "Conversión Celsius-Fahrenheit",
                "Regresión lineal simple",
                "Prototipado rápido",
                "Baseline para comparación"
            ],
            complexity="simple",
            estimated_training_time="< 1 minuto"
        )
    
    @staticmethod
    def get_shallow_neural_network() -> ModelTemplate:
        """Plantilla para red neuronal poco profunda."""
        return ModelTemplate(
            name="shallow_neural_network",
            description="Red neuronal con una capa oculta para regresión no lineal",
            architecture={
                "layers": [16, 1],
                "activation": "relu",
                "dropout_rate": 0.1,
                "batch_normalization": False
            },
            training_params={
                "epochs": 150,
                "learning_rate": 0.001,
                "batch_size": 32,
                "validation_split": 0.2,
                "early_stopping": True,
                "patience": 15
            },
            use_cases=[
                "Regresión no lineal simple",
                "Patrones básicos en datos",
                "Mejora sobre modelo lineal",
                "Aprendizaje de características simples"
            ],
            complexity="simple",
            estimated_training_time="1-2 minutos"
        )
    
    @staticmethod
    def get_deep_regression() -> ModelTemplate:
        """Plantilla para regresión profunda."""
        return ModelTemplate(
            name="deep_regression",
            description="Red neuronal profunda con múltiples capas ocultas",
            architecture={
                "layers": [64, 32, 16, 1],
                "activation": "relu",
                "dropout_rate": 0.2,
                "batch_normalization": True
            },
            training_params={
                "epochs": 200,
                "learning_rate": 0.001,
                "batch_size": 64,
                "validation_split": 0.2,
                "early_stopping": True,
                "patience": 20
            },
            use_cases=[
                "Patrones complejos en datos",
                "Regresión no lineal avanzada",
                "Datasets con ruido",
                "Máximo rendimiento"
            ],
            complexity="medium",
            estimated_training_time="3-5 minutos"
        )
    
    @staticmethod
    def get_regularized_network() -> ModelTemplate:
        """Plantilla para red con regularización fuerte."""
        return ModelTemplate(
            name="regularized_network",
            description="Red neuronal con regularización fuerte para evitar overfitting",
            architecture={
                "layers": [32, 16, 8, 1],
                "activation": "relu",
                "dropout_rate": 0.3,
                "batch_normalization": True
            },
            training_params={
                "epochs": 300,
                "learning_rate": 0.0005,
                "batch_size": 32,
                "validation_split": 0.3,
                "early_stopping": True,
                "patience": 25
            },
            use_cases=[
                "Datasets pequeños",
                "Prevención de overfitting",
                "Generalización robusta",
                "Entrenamiento estable"
            ],
            complexity="medium",
            estimated_training_time="4-6 minutos"
        )
    
    @staticmethod
    def get_fast_prototype() -> ModelTemplate:
        """Plantilla para prototipado rápido."""
        return ModelTemplate(
            name="fast_prototype",
            description="Configuración optimizada para pruebas rápidas y desarrollo",
            architecture={
                "layers": [8, 1],
                "activation": "relu",
                "dropout_rate": 0.0,
                "batch_normalization": False
            },
            training_params={
                "epochs": 50,
                "learning_rate": 0.01,
                "batch_size": 64,
                "validation_split": 0.2,
                "early_stopping": False,
                "patience": 10
            },
            use_cases=[
                "Desarrollo y debugging",
                "Pruebas de concepto",
                "Validación rápida de ideas",
                "Testing de pipeline"
            ],
            complexity="simple",
            estimated_training_time="< 30 segundos"
        )
    
    @staticmethod
    def get_robust_production() -> ModelTemplate:
        """Plantilla para modelo robusto de producción."""
        return ModelTemplate(
            name="robust_production",
            description="Configuración robusta y estable para entornos de producción",
            architecture={
                "layers": [128, 64, 32, 16, 1],
                "activation": "relu",
                "dropout_rate": 0.15,
                "batch_normalization": True
            },
            training_params={
                "epochs": 500,
                "learning_rate": 0.0001,
                "batch_size": 128,
                "validation_split": 0.25,
                "early_stopping": True,
                "patience": 50
            },
            use_cases=[
                "Modelos de producción",
                "Máxima precisión",
                "Estabilidad a largo plazo",
                "Datasets grandes"
            ],
            complexity="complex",
            estimated_training_time="8-12 minutos"
        )
    
    @classmethod
    def get_all_templates(cls) -> Dict[str, ModelTemplate]:
        """
        Obtiene todas las plantillas disponibles.
        
        Returns:
            Diccionario con todas las plantillas indexadas por nombre
        """
        return {
            "simple_regression": cls.get_simple_regression(),
            "shallow_neural_network": cls.get_shallow_neural_network(),
            "deep_regression": cls.get_deep_regression(),
            "regularized_network": cls.get_regularized_network(),
            "fast_prototype": cls.get_fast_prototype(),
            "robust_production": cls.get_robust_production()
        }
    
    @classmethod
    def get_templates_by_complexity(cls, complexity: str) -> Dict[str, ModelTemplate]:
        """
        Filtra plantillas por nivel de complejidad.
        
        Args:
            complexity: Nivel de complejidad ('simple', 'medium', 'complex')
            
        Returns:
            Diccionario con plantillas filtradas
        """
        all_templates = cls.get_all_templates()
        return {
            name: template for name, template in all_templates.items()
            if template.complexity == complexity
        }
    
    @classmethod
    def get_templates_by_use_case(cls, use_case: str) -> Dict[str, ModelTemplate]:
        """
        Filtra plantillas por caso de uso.
        
        Args:
            use_case: Caso de uso a buscar
            
        Returns:
            Diccionario con plantillas que coinciden con el caso de uso
        """
        all_templates = cls.get_all_templates()
        return {
            name: template for name, template in all_templates.items()
            if any(use_case.lower() in uc.lower() for uc in template.use_cases)
        }
    
    @classmethod
    def get_template_recommendations(cls, requirements: Dict[str, Any]) -> List[str]:
        """
        Recomienda plantillas basadas en requerimientos.
        
        Args:
            requirements: Diccionario con requerimientos del usuario
            
        Returns:
            Lista de nombres de plantillas recomendadas
        """
        recommendations = []
        
        # Recomendaciones basadas en tiempo disponible
        time_constraint = requirements.get('max_training_time', 'medium')
        if time_constraint == 'fast':
            recommendations.extend(['fast_prototype', 'simple_regression'])
        elif time_constraint == 'medium':
            recommendations.extend(['shallow_neural_network', 'deep_regression'])
        else:
            recommendations.extend(['robust_production', 'regularized_network'])
        
        # Recomendaciones basadas en experiencia
        experience = requirements.get('user_experience', 'beginner')
        if experience == 'beginner':
            recommendations.insert(0, 'simple_regression')
        elif experience == 'advanced':
            recommendations.insert(0, 'robust_production')
        
        # Recomendaciones basadas en objetivo
        objective = requirements.get('objective', 'learning')
        if objective == 'production':
            recommendations.insert(0, 'robust_production')
        elif objective == 'experimentation':
            recommendations.insert(0, 'deep_regression')
        
        # Eliminar duplicados manteniendo orden
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:3]  # Máximo 3 recomendaciones