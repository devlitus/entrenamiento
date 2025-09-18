# backend/src/services/statistics/trend_analyzer.py

import sqlite3
import time
from typing import Dict, List, Any, Tuple

class TrendAnalyzer:
    """Servicio para análisis de tendencias y rendimiento temporal"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_trend_analysis(self, period: str, days_back: int) -> Dict[str, Any]:
        """Analiza tendencias de rendimiento en el tiempo"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Determinar el agrupamiento temporal
            if period == 'daily':
                time_format = '%Y-%m-%d'
                seconds_per_period = 86400
            elif period == 'weekly':
                time_format = '%Y-W%W'
                seconds_per_period = 604800
            else:  # monthly
                time_format = '%Y-%m'
                seconds_per_period = 2592000
            
            cutoff_time = time.time() - (days_back * 24 * 60 * 60)
            
            cursor.execute('''
                SELECT 
                    DATE(t.start_time, 'unixepoch') as date,
                    AVG(em.val_loss) as avg_performance,
                    COUNT(DISTINCT t.id) as training_count,
                    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) * 100.0 / COUNT(*) as success_rate
                FROM trainings t
                LEFT JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ?
                AND em.epoch = (SELECT MAX(epoch) FROM epoch_metrics em2 WHERE em2.training_id = t.id)
                GROUP BY DATE(t.start_time, 'unixepoch')
                ORDER BY date
            ''', (cutoff_time,))
            
            data_points = []
            performances = []
            
            for row in cursor.fetchall():
                point = {
                    'date': row[0],
                    'avg_performance': round(row[1] or 0, 6),
                    'training_count': row[2],
                    'success_rate': round(row[3] or 0, 2)
                }
                data_points.append(point)
                if row[1]:
                    performances.append(row[1])
            
            # Calcular tendencia
            trend_direction, trend_strength = self._calculate_trend(performances)
            insights = self._generate_trend_insights(data_points, trend_direction, trend_strength)
            
            return {
                'period': period,
                'data_points': data_points,
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'insights': insights
            }
    
    def get_performance_over_time(self, days_back: int) -> List[Dict[str, Any]]:
        """Obtiene datos de rendimiento a lo largo del tiempo para gráficos"""
        cutoff_time = time.time() - (days_back * 24 * 60 * 60)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    DATE(t.start_time, 'unixepoch') as date,
                    AVG(em.val_loss) as avg_loss,
                    COUNT(DISTINCT t.id) as session_count
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ?
                AND em.epoch = (SELECT MAX(epoch) FROM epoch_metrics em2 WHERE em2.training_id = t.id)
                GROUP BY DATE(t.start_time, 'unixepoch')
                ORDER BY date
            ''', (cutoff_time,))
            
            return [{
                'date': row[0],
                'avg_loss': round(row[1], 6) if row[1] else 0,
                'session_count': row[2]
            } for row in cursor.fetchall()]
    
    def _calculate_trend(self, values: List[float]) -> Tuple[str, float]:
        """Calcula la tendencia de una serie de valores"""
        if len(values) < 2:
            return 'stable', 0.0
        
        # Regresión lineal simple
        n = len(values)
        x = list(range(n))
        slope = (n * sum(x[i] * values[i] for i in range(n)) - sum(x) * sum(values)) / \
                (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
        
        if abs(slope) < 0.001:
            return 'stable', abs(slope)
        elif slope > 0:
            return 'declining', abs(slope)  # Para loss, mayor es peor
        else:
            return 'improving', abs(slope)
    
    def _generate_trend_insights(self, data_points: List[Dict], direction: str, strength: float) -> List[str]:
        """Genera insights basados en tendencias"""
        insights = []
        
        if direction == 'improving' and strength > 0.01:
            insights.append("El rendimiento del modelo está mejorando consistentemente")
        elif direction == 'declining' and strength > 0.01:
            insights.append("Se detecta una tendencia de empeoramiento en el rendimiento")
        else:
            insights.append("El rendimiento se mantiene estable")
        
        # Análisis adicional de patrones
        if len(data_points) >= 7:
            recent_success_rates = [point['success_rate'] for point in data_points[-7:]]
            avg_recent_success = sum(recent_success_rates) / len(recent_success_rates)
            
            if avg_recent_success < 70:
                insights.append("La tasa de éxito ha disminuido en los últimos días")
            elif avg_recent_success > 90:
                insights.append("Excelente tasa de éxito mantenida recientemente")
        
        return insights