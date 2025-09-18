# backend/src/services/metrics_storage_refactored.py

from typing import Dict, List, Any, Optional
from .storage import DatabaseManager, TrainingManager, MetricsCollector, StatisticsAnalyzer


class MetricsStorage:
    """Servicio refactorizado para almacenar y recuperar métricas históricas"""
    
    def __init__(self, db_path: str = 'data/metrics.db'):
        self.db_manager = DatabaseManager(db_path)
        self.training_manager = TrainingManager(self.db_manager)
        self.metrics_collector = MetricsCollector(self.db_manager)
        self.statistics_analyzer = StatisticsAnalyzer(self.db_manager)
    
    # Métodos de gestión de entrenamientos
    def create_training_session(self, name: str, hyperparameters: Dict[str, Any], 
                               model_type: str = 'regression') -> int:
        """Crea una nueva sesión de entrenamiento"""
        return self.training_manager.create_training_session(name, hyperparameters, model_type)
    
    def update_training_status(self, training_id: int, status: str, 
                              final_loss: Optional[float] = None, 
                              epochs: Optional[int] = None):
        """Actualiza el estado de un entrenamiento"""
        self.training_manager.update_training_status(training_id, status, final_loss, epochs)
    
    def finish_training_session(self, training_id: int, status: str = 'completed', 
                               final_loss: Optional[float] = None, epochs: Optional[int] = None):
        """Finaliza una sesión de entrenamiento"""
        self.update_training_status(training_id, status, final_loss, epochs)
    
    def get_training_sessions_with_filters(self, days: int = 30, status: Optional[str] = None, 
                                         limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene sesiones de entrenamiento con filtros"""
        return self.training_manager.get_training_sessions_with_filters(days, status, limit)
    
    def get_training_summary(self, training_id: int) -> Dict[str, Any]:
        """Obtiene un resumen completo de un entrenamiento"""
        summary = self.training_manager.get_training_summary(training_id)
        if summary:
            # Agregar métricas y alertas
            summary['metrics'] = self.metrics_collector.get_training_metrics(training_id)
            summary['alerts'] = self.metrics_collector.get_alerts(training_id)
            
            # Estadísticas de hardware
            hardware_metrics = self.metrics_collector.get_hardware_metrics(training_id)
            if hardware_metrics:
                summary['hardware_summary'] = {
                    'avg_cpu_usage': sum(m['cpu_usage'] or 0 for m in hardware_metrics) / len(hardware_metrics),
                    'avg_memory_usage': sum(m['memory_usage'] or 0 for m in hardware_metrics) / len(hardware_metrics),
                    'max_temperature': max((m['temperature'] or 0 for m in hardware_metrics), default=0)
                }
        return summary
    
    def export_training_data(self, training_id: int, filepath: str):
        """Exporta todos los datos de un entrenamiento a JSON"""
        self.training_manager.export_training_data(training_id, filepath)
    
    # Métodos de recolección de métricas
    def store_epoch_metrics(self, training_id: int, epoch: int, metrics: Dict[str, Any]):
        """Almacena métricas de una época específica"""
        self.metrics_collector.store_epoch_metrics(training_id, epoch, metrics)
    
    def store_hardware_metrics(self, training_id: Optional[int], hardware_data: Dict[str, Any]):
        """Almacena métricas de hardware"""
        self.metrics_collector.store_hardware_metrics(training_id, hardware_data)
    
    def store_alert(self, alert_id: str, training_id: Optional[int], alert_type: str,
                   level: str, title: str, message: str, data: Optional[Dict[str, Any]] = None):
        """Almacena una alerta"""
        self.metrics_collector.store_alert(alert_id, training_id, alert_type, level, title, message, data)
    
    def get_training_metrics(self, training_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las métricas de un entrenamiento"""
        return self.metrics_collector.get_training_metrics(training_id)
    
    def get_hardware_metrics(self, training_id: Optional[int] = None, 
                           hours: int = 24) -> List[Dict[str, Any]]:
        """Obtiene métricas de hardware"""
        return self.metrics_collector.get_hardware_metrics(training_id, hours)
    
    def get_alerts(self, training_id: Optional[int] = None, 
                  resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene alertas"""
        return self.metrics_collector.get_alerts(training_id, resolved)
    
    # Métodos de análisis estadístico
    def get_aggregated_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Obtiene estadísticas agregadas de entrenamientos"""
        return self.statistics_analyzer.get_aggregated_statistics(days)
    
    def get_trend_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Analiza tendencias en los entrenamientos"""
        return self.statistics_analyzer.get_trend_analysis(days)
    
    def get_performance_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Obtiene métricas de rendimiento del sistema"""
        return self.statistics_analyzer.get_performance_metrics(days)
    
    # Métodos de mantenimiento
    def cleanup_old_data(self, days: int = 30):
        """Limpia datos antiguos de la base de datos"""
        self.db_manager.cleanup_old_data(days)