# backend/src/services/statistics_service.py

from typing import Dict, List, Any, Optional
from .statistics.dashboard_data_service import DashboardDataService
from .statistics.trend_analyzer import TrendAnalyzer
from .statistics.efficiency_calculator import EfficiencyCalculator
from .statistics.insights_generator import InsightsGenerator
from .statistics.convergence_analyzer import ConvergenceAnalyzer

class StatisticsService:
    """Servicio principal de estadísticas que coordina los módulos especializados"""
    
    def __init__(self, metrics_storage):
        self.metrics_storage = metrics_storage
        self.db_path = metrics_storage.db_manager.db_path
        
        # Inicializar módulos especializados
        self.dashboard_service = DashboardDataService(self.db_path)
        self.trend_analyzer = TrendAnalyzer(self.db_path)
        self.efficiency_calculator = EfficiencyCalculator(self.db_path)
        self.insights_generator = InsightsGenerator(self.db_path)
        self.convergence_analyzer = ConvergenceAnalyzer(self.db_path)
    
    # === Métodos del Dashboard ===
    def get_dashboard_data(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene datos completos para el dashboard"""
        return self.dashboard_service.get_dashboard_data(since_timestamp)
    
    def get_aggregated_stats(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene estadísticas agregadas"""
        return self.dashboard_service.get_aggregated_stats(since_timestamp)
    
    def get_recent_training_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene sesiones de entrenamiento recientes"""
        return self.dashboard_service.get_recent_training_sessions(limit)
    
    # === Métodos de Análisis de Tendencias ===
    def get_trend_analysis(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene análisis de tendencias"""
        return self.trend_analyzer.get_trend_analysis(since_timestamp)
    
    def get_performance_over_time(self, since_timestamp: float) -> List[Dict[str, Any]]:
        """Obtiene rendimiento a lo largo del tiempo"""
        return self.trend_analyzer.get_performance_over_time(since_timestamp)
    
    # === Métodos de Eficiencia ===
    def get_efficiency_metrics(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene métricas de eficiencia"""
        return self.efficiency_calculator.get_efficiency_metrics(since_timestamp)
    
    # === Métodos de Insights ===
    def generate_auto_insights(self, since_timestamp: float) -> List[Dict[str, Any]]:
        """Genera insights automáticos"""
        return self.insights_generator.generate_auto_insights(since_timestamp)
    
    def get_hyperparameter_performance_map(self, since_timestamp: float) -> Dict[str, Any]:
        """Obtiene mapa de rendimiento de hiperparámetros"""
        return self.insights_generator.get_hyperparameter_performance_map(since_timestamp)
    
    # === Métodos de Convergencia ===
    def get_top_performing_sessions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtiene las sesiones con mejor rendimiento"""
        return self.convergence_analyzer.get_top_performing_sessions(limit)
    
    # === Métodos Privados de Compatibilidad ===
    def _analyze_convergence_patterns(self, since_timestamp: float) -> Dict[str, Any]:
        """Analiza patrones de convergencia (método de compatibilidad)"""
        return self.convergence_analyzer.analyze_convergence_patterns(since_timestamp)
    
    def _get_final_metrics(self, training_id: int) -> Optional[Dict[str, float]]:
        """Obtiene métricas finales de un entrenamiento (método de compatibilidad)"""
        return self.dashboard_service._get_final_metrics(training_id)
    
    def _get_best_metrics(self, training_id: int) -> Optional[Dict[str, float]]:
        """Obtiene las mejores métricas de un entrenamiento (método de compatibilidad)"""
        return self.dashboard_service._get_best_metrics(training_id)
    
    def _get_alerts_summary(self, since_timestamp: float) -> Dict[str, int]:
        """Obtiene resumen de alertas (método de compatibilidad)"""
        return self.dashboard_service._get_alerts_summary(since_timestamp)
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendencia de una lista de valores (método de compatibilidad)"""
        return self.trend_analyzer._calculate_trend(values)
    
    def _generate_trend_insights(self, trend_data: Dict[str, Any]) -> List[str]:
        """Genera insights de tendencias (método de compatibilidad)"""
        return self.trend_analyzer._generate_trend_insights(trend_data)