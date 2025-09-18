# backend/src/services/statistics_service_optimized.py
"""
Servicio de estadísticas optimizado usando patrón Strategy.

Esta versión optimizada del StatisticsService utiliza el patrón Strategy
para delegar responsabilidades específicas a estrategias especializadas.
"""

from typing import Dict, List, Any, Optional
from utils.logger import setup_logger

# Importar estrategias
from .statistics.base_strategy import StatisticsStrategy
from .statistics.dashboard_strategy import DashboardStrategy
from .statistics.trends_strategy import TrendsStrategy
from .statistics.efficiency_calculator import EfficiencyCalculator
from .statistics.insights_generator import InsightsGenerator

logger = setup_logger()

class StatisticsServiceOptimized:
    """Servicio de estadísticas optimizado con patrón Strategy.
    
    Este servicio coordina diferentes estrategias de análisis estadístico,
    reduciendo la complejidad y mejorando la mantenibilidad del código.
    
    Attributes:
        strategies: Diccionario de estrategias disponibles
        db_path: Ruta a la base de datos de métricas
    """
    
    def __init__(self, metrics_storage):
        """Inicializa el servicio optimizado.
        
        Args:
            metrics_storage: Instancia del almacén de métricas
        """
        self.metrics_storage = metrics_storage
        self.db_path = metrics_storage.db_manager.db_path
        
        # Inicializar estrategias
        self.strategies = {
            'dashboard': DashboardStrategy(self.db_path),
            'trends': TrendsStrategy(self.db_path)
        }
        
        # Servicios especializados (no convertidos a Strategy aún)
        self.efficiency_calculator = EfficiencyCalculator(self.db_path)
        self.insights_generator = InsightsGenerator(self.db_path)
        
        logger.info("StatisticsService optimizado inicializado con patrón Strategy")
    
    def execute_strategy(self, strategy_name: str, **kwargs) -> Dict[str, Any]:
        """Ejecuta una estrategia específica.
        
        Args:
            strategy_name: Nombre de la estrategia a ejecutar
            **kwargs: Parámetros para la estrategia
            
        Returns:
            Resultado de la estrategia ejecutada
            
        Raises:
            ValueError: Si la estrategia no existe
        """
        if strategy_name not in self.strategies:
            available = ', '.join(self.strategies.keys())
            raise ValueError(f"Estrategia '{strategy_name}' no disponible. Disponibles: {available}")
        
        strategy = self.strategies[strategy_name]
        
        # Validar parámetros
        if not strategy.validate_parameters(**kwargs):
            raise ValueError(f"Parámetros inválidos para estrategia '{strategy_name}'")
        
        logger.info(f"Ejecutando estrategia: {strategy_name}")
        return strategy.execute(**kwargs)
    
    # === Métodos de compatibilidad con API existente ===
    
    def get_dashboard_data(self, since_timestamp: float = 0.0) -> Dict[str, Any]:
        """Obtiene datos del dashboard usando estrategia optimizada."""
        return self.execute_strategy('dashboard', since_timestamp=since_timestamp)
    
    def get_trend_analysis(self, since_timestamp: float = 0.0) -> Dict[str, Any]:
        """Obtiene análisis de tendencias usando estrategia optimizada."""
        return self.execute_strategy('trends', since_timestamp=since_timestamp)
    
    def get_efficiency_metrics(self, since_timestamp: float = 0.0) -> Dict[str, Any]:
        """Obtiene métricas de eficiencia."""
        return self.efficiency_calculator.get_efficiency_metrics(since_timestamp)
    
    def generate_auto_insights(self, since_timestamp: float = 0.0) -> List[Dict[str, Any]]:
        """Genera insights automáticos."""
        return self.insights_generator.generate_auto_insights(since_timestamp)
    
    def get_hyperparameter_performance_map(self, since_timestamp: float = 0.0) -> Dict[str, Any]:
        """Obtiene mapa de rendimiento de hiperparámetros."""
        return self.insights_generator.get_hyperparameter_performance_map(since_timestamp)
    
    # === Métodos de gestión de estrategias ===
    
    def register_strategy(self, name: str, strategy: StatisticsStrategy) -> None:
        """Registra una nueva estrategia.
        
        Args:
            name: Nombre de la estrategia
            strategy: Instancia de la estrategia
        """
        self.strategies[name] = strategy
        logger.info(f"Estrategia '{name}' registrada exitosamente")
    
    def get_available_strategies(self) -> List[str]:
        """Obtiene lista de estrategias disponibles.
        
        Returns:
            Lista de nombres de estrategias disponibles
        """
        return list(self.strategies.keys())
    
    def get_strategy_info(self, strategy_name: str) -> Dict[str, str]:
        """Obtiene información de una estrategia.
        
        Args:
            strategy_name: Nombre de la estrategia
            
        Returns:
            Información de la estrategia
        """
        if strategy_name not in self.strategies:
            return {'error': f"Estrategia '{strategy_name}' no encontrada"}
        
        strategy = self.strategies[strategy_name]
        return {
            'name': strategy.get_strategy_name(),
            'class': strategy.__class__.__name__,
            'available': True
        }