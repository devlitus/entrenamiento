# backend/src/services/storage/statistics_analyzer.py

import sqlite3
import time
from typing import Dict, List, Any, Optional
from .database_manager import DatabaseManager


class StatisticsAnalyzer:
    """Analizador de estadísticas y tendencias de entrenamientos"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_aggregated_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Obtiene estadísticas agregadas de entrenamientos"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Estadísticas básicas
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_trainings,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_trainings,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_trainings,
                    AVG(CASE WHEN final_loss IS NOT NULL THEN final_loss END) as avg_final_loss,
                    MIN(CASE WHEN final_loss IS NOT NULL THEN final_loss END) as best_loss,
                    AVG(CASE WHEN duration IS NOT NULL THEN duration END) as avg_duration,
                    AVG(CASE WHEN epochs IS NOT NULL THEN epochs END) as avg_epochs
                FROM trainings 
                WHERE start_time > ?
            ''', (cutoff_time,))
            
            stats = dict(cursor.fetchone())
            
            # Calcular tasa de éxito
            if stats['total_trainings'] > 0:
                stats['success_rate'] = stats['completed_trainings'] / stats['total_trainings']
            else:
                stats['success_rate'] = 0.0
            
            return stats
    
    def get_trend_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Analiza tendencias en los entrenamientos"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obtener entrenamientos ordenados por fecha
            cursor.execute('''
                SELECT final_loss, duration, epochs, start_time
                FROM trainings 
                WHERE start_time > ? AND status = 'completed' AND final_loss IS NOT NULL
                ORDER BY start_time ASC
            ''', (cutoff_time,))
            
            trainings = cursor.fetchall()
            
            if len(trainings) < 2:
                return {
                    'loss_trend': 'insufficient_data',
                    'avg_duration': None,
                    'avg_epochs': None,
                    'period': 'monthly'
                }
            
            # Analizar tendencia de loss
            losses = [t['final_loss'] for t in trainings]
            first_half = losses[:len(losses)//2]
            second_half = losses[len(losses)//2:]
            
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)
            
            if avg_second < avg_first * 0.95:
                loss_trend = 'improving'
            elif avg_second > avg_first * 1.05:
                loss_trend = 'degrading'
            else:
                loss_trend = 'stable'
            
            # Calcular promedios
            avg_duration = sum(t['duration'] for t in trainings if t['duration']) / len(trainings)
            avg_epochs = sum(t['epochs'] for t in trainings if t['epochs']) / len(trainings)
            
            return {
                'loss_trend': loss_trend,
                'avg_duration': avg_duration,
                'avg_epochs': avg_epochs,
                'period': 'monthly',
                'sample_size': len(trainings)
            }
    
    def get_performance_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Obtiene métricas de rendimiento del sistema"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Métricas de hardware promedio
            cursor.execute('''
                SELECT 
                    AVG(cpu_usage) as avg_cpu,
                    AVG(memory_usage) as avg_memory,
                    AVG(gpu_usage) as avg_gpu,
                    AVG(temperature) as avg_temp,
                    MAX(temperature) as max_temp
                FROM hardware_metrics 
                WHERE timestamp > ?
            ''', (cutoff_time,))
            
            hardware_stats = dict(cursor.fetchone())
            
            # Conteo de alertas por tipo
            cursor.execute('''
                SELECT type, level, COUNT(*) as count
                FROM alerts 
                WHERE timestamp > ?
                GROUP BY type, level
            ''', (cutoff_time,))
            
            alert_stats = {}
            for row in cursor.fetchall():
                alert_type = row['type']
                if alert_type not in alert_stats:
                    alert_stats[alert_type] = {}
                alert_stats[alert_type][row['level']] = row['count']
            
            return {
                'hardware': hardware_stats,
                'alerts': alert_stats,
                'period_days': days
            }