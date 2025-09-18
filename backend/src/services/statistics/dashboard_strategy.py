# backend/src/services/statistics/dashboard_strategy.py
"""
Estrategia para análisis de datos del dashboard.

Implementa la lógica específica para generar datos del dashboard
siguiendo el patrón Strategy.
"""

from typing import Dict, List, Any, Optional
from .base_strategy import StatisticsStrategy
from .dashboard_data_service import DashboardDataService

class DashboardStrategy(StatisticsStrategy):
    """Estrategia para análisis de datos del dashboard."""
    
    def __init__(self, db_path: str):
        """Inicializa la estrategia del dashboard.
        
        Args:
            db_path: Ruta a la base de datos de métricas
        """
        super().__init__(db_path)
        self.dashboard_service = DashboardDataService(db_path)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Ejecuta el análisis de datos del dashboard.
        
        Args:
            **kwargs: Parámetros que pueden incluir:
                - since_timestamp: Timestamp desde el cual obtener datos
                - include_aggregated: Si incluir estadísticas agregadas
                - include_sessions: Si incluir sesiones recientes
                
        Returns:
            Datos completos del dashboard
        """
        since_timestamp = kwargs.get('since_timestamp', 0.0)
        include_aggregated = kwargs.get('include_aggregated', True)
        include_sessions = kwargs.get('include_sessions', True)
        
        result = {}
        
        # Datos principales del dashboard
        result.update(self.dashboard_service.get_dashboard_data(since_timestamp))
        
        # Estadísticas agregadas opcionales
        if include_aggregated:
            result['aggregated_stats'] = self.dashboard_service.get_aggregated_stats(since_timestamp)
        
        # Sesiones recientes opcionales
        if include_sessions:
            limit = kwargs.get('sessions_limit', 10)
            result['recent_sessions'] = self.dashboard_service.get_recent_training_sessions(limit)
        
        return result
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia.
        
        Returns:
            Nombre de la estrategia
        """
        return "dashboard"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Valida los parámetros específicos del dashboard.
        
        Args:
            **kwargs: Parámetros a validar
            
        Returns:
            True si los parámetros son válidos
        """
        since_timestamp = kwargs.get('since_timestamp', 0.0)
        sessions_limit = kwargs.get('sessions_limit', 10)
        
        if not isinstance(since_timestamp, (int, float)) or since_timestamp < 0:
            return False
        
        if not isinstance(sessions_limit, int) or sessions_limit < 1 or sessions_limit > 100:
            return False
        
        return True