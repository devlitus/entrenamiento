# backend/src/services/statistics/trends_strategy.py
"""
Estrategia para análisis de tendencias.

Implementa la lógica específica para análisis de tendencias
siguiendo el patrón Strategy.
"""

from typing import Dict, List, Any
from .base_strategy import StatisticsStrategy
from .trend_analyzer import TrendAnalyzer

class TrendsStrategy(StatisticsStrategy):
    """Estrategia para análisis de tendencias."""
    
    def __init__(self, db_path: str):
        """Inicializa la estrategia de tendencias.
        
        Args:
            db_path: Ruta a la base de datos de métricas
        """
        super().__init__(db_path)
        self.trend_analyzer = TrendAnalyzer(db_path)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Ejecuta el análisis de tendencias.
        
        Args:
            **kwargs: Parámetros que pueden incluir:
                - since_timestamp: Timestamp desde el cual analizar
                - include_performance: Si incluir rendimiento temporal
                - analysis_depth: Profundidad del análisis ('basic', 'detailed')
                
        Returns:
            Análisis completo de tendencias
        """
        since_timestamp = kwargs.get('since_timestamp', 0.0)
        include_performance = kwargs.get('include_performance', True)
        analysis_depth = kwargs.get('analysis_depth', 'basic')
        
        result = {}
        
        # Análisis principal de tendencias
        result.update(self.trend_analyzer.get_trend_analysis(since_timestamp))
        
        # Rendimiento temporal opcional
        if include_performance:
            result['performance_over_time'] = self.trend_analyzer.get_performance_over_time(since_timestamp)
        
        # Análisis detallado opcional
        if analysis_depth == 'detailed':
            result['detailed_insights'] = self._get_detailed_insights(since_timestamp)
        
        return result
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia.
        
        Returns:
            Nombre de la estrategia
        """
        return "trends"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Valida los parámetros específicos de tendencias.
        
        Args:
            **kwargs: Parámetros a validar
            
        Returns:
            True si los parámetros son válidos
        """
        since_timestamp = kwargs.get('since_timestamp', 0.0)
        analysis_depth = kwargs.get('analysis_depth', 'basic')
        
        if not isinstance(since_timestamp, (int, float)) or since_timestamp < 0:
            return False
        
        if analysis_depth not in ['basic', 'detailed']:
            return False
        
        return True
    
    def _get_detailed_insights(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene insights detallados de tendencias.
        
        Args:
            since_timestamp: Timestamp desde el cual analizar
            
        Returns:
            Insights detallados
        """
        # Implementación de análisis detallado
        return {
            'convergence_patterns': self.trend_analyzer._analyze_convergence_patterns(since_timestamp),
            'performance_stability': self.trend_analyzer._analyze_performance_stability(since_timestamp),
            'optimization_suggestions': self.trend_analyzer._generate_optimization_suggestions(since_timestamp)
        }