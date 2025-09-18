# backend/src/services/statistics/base_strategy.py
"""
Interfaz base para estrategias de análisis estadístico.

Define el contrato común para todas las estrategias de análisis,
implementando el patrón Strategy para optimizar StatisticsService.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class StatisticsStrategy(ABC):
    """Interfaz base para estrategias de análisis estadístico.
    
    Esta clase abstracta define el contrato que deben cumplir todas
    las estrategias de análisis estadístico del sistema.
    """
    
    def __init__(self, db_path: str):
        """Inicializa la estrategia con la ruta de la base de datos.
        
        Args:
            db_path: Ruta a la base de datos de métricas
        """
        self.db_path = db_path
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Ejecuta la estrategia de análisis.
        
        Args:
            **kwargs: Parámetros específicos de la estrategia
            
        Returns:
            Resultado del análisis estadístico
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia.
        
        Returns:
            Nombre identificativo de la estrategia
        """
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Valida los parámetros de entrada.
        
        Args:
            **kwargs: Parámetros a validar
            
        Returns:
            True si los parámetros son válidos
        """
        return True