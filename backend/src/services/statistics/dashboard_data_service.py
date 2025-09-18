# backend/src/services/statistics/dashboard_data_service.py

import sqlite3
import json
import time
from typing import Dict, List, Any
from datetime import datetime

class DashboardDataService:
    """Servicio para generar datos agregados del dashboard de estadísticas"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_dashboard_data(self, days_back: int = 30) -> Dict[str, Any]:
        """Obtiene todos los datos necesarios para el dashboard de estadísticas"""
        cutoff_time = time.time() - (days_back * 24 * 60 * 60)
        
        return {
            'aggregated_stats': self.get_aggregated_stats(cutoff_time),
            'recent_sessions': self.get_recent_training_sessions(limit=10)
        }
    
    def get_aggregated_stats(self, since_timestamp: float = 0) -> Dict[str, Any]:
        """Calcula estadísticas agregadas de todos los entrenamientos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Estadísticas básicas de entrenamientos
            cursor.execute('''
                SELECT COUNT(*) as total,
                       COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                       AVG(CASE WHEN end_time IS NOT NULL THEN end_time - start_time END) as avg_duration,
                       SUM(CASE WHEN end_time IS NOT NULL THEN end_time - start_time ELSE 0 END) as total_time
                FROM trainings 
                WHERE start_time >= ?
            ''', (since_timestamp,))
            
            stats = cursor.fetchone()
            total_trainings = stats[0] or 0
            completed_trainings = stats[1] or 0
            avg_duration = stats[2] or 0
            total_time = stats[3] or 0
            
            success_rate = (completed_trainings / total_trainings * 100) if total_trainings > 0 else 0
            
            # Métricas de rendimiento
            cursor.execute('''
                SELECT 
                    AVG(em.val_loss) as avg_final_loss,
                    MIN(em.val_loss) as best_loss,
                    MAX(em.val_loss) as worst_loss
                FROM epoch_metrics em
                JOIN trainings t ON em.training_id = t.id
                WHERE t.start_time >= ? AND t.status = 'completed'
                AND em.epoch = (
                    SELECT MAX(epoch) FROM epoch_metrics em2 
                    WHERE em2.training_id = em.training_id
                )
            ''', (since_timestamp,))
            
            metrics = cursor.fetchone()
            
            return {
                'total_trainings': total_trainings,
                'total_training_time': int(total_time),
                'average_training_time': int(avg_duration),
                'success_rate': round(success_rate, 2),
                'metrics_summary': {
                    'avg_final_loss': round(metrics[0] or 0, 6),
                    'best_loss_achieved': round(metrics[1] or 0, 6),
                    'worst_loss_achieved': round(metrics[2] or 0, 6)
                }
            }
    
    def get_recent_training_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene las sesiones de entrenamiento más recientes con detalles completos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT t.id, t.name, t.start_time, t.end_time, t.status, 
                       t.hyperparameters, t.model_type
                FROM trainings t
                ORDER BY t.start_time DESC
                LIMIT ?
            ''', (limit,))
            
            sessions = []
            for row in cursor.fetchall():
                session_id = row[0]
                
                # Obtener métricas finales
                final_metrics = self._get_final_metrics(session_id)
                best_metrics = self._get_best_metrics(session_id)
                alerts_summary = self._get_alerts_summary(session_id)
                
                duration = None
                if row[3]:  # end_time exists
                    duration = int(row[3] - row[2])
                
                hyperparams = json.loads(row[5]) if row[5] else {}
                
                sessions.append({
                    'id': session_id,
                    'start_time': datetime.fromtimestamp(row[2]).isoformat(),
                    'end_time': datetime.fromtimestamp(row[3]).isoformat() if row[3] else None,
                    'duration_seconds': duration,
                    'total_epochs': self._get_total_epochs(session_id),
                    'hyperparameters': {
                        'learning_rate': hyperparams.get('learning_rate', 0),
                        'batch_size': hyperparams.get('batch_size', 0),
                        'epochs': hyperparams.get('epochs', 0),
                        'training_data_size': hyperparams.get('training_data_size', 0)
                    },
                    'final_metrics': final_metrics,
                    'best_metrics': best_metrics,
                    'alerts_summary': alerts_summary
                })
            
            return sessions
    
    def _get_final_metrics(self, training_id: int) -> Dict[str, float]:
        """Obtiene las métricas finales de un entrenamiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT loss, val_loss, mae, val_mae
                FROM epoch_metrics
                WHERE training_id = ?
                ORDER BY epoch DESC
                LIMIT 1
            ''', (training_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'train_loss': result[0] or 0,
                    'val_loss': result[1] or 0,
                    'train_mae': result[2] or 0,
                    'val_mae': result[3] or 0
                }
            return {'train_loss': 0, 'val_loss': 0, 'train_mae': 0, 'val_mae': 0}
    
    def _get_best_metrics(self, training_id: int) -> Dict[str, Any]:
        """Obtiene las mejores métricas alcanzadas durante el entrenamiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT MIN(val_loss) as best_val_loss, epoch
                FROM epoch_metrics
                WHERE training_id = ? AND val_loss IS NOT NULL
                ORDER BY val_loss ASC
                LIMIT 1
            ''', (training_id,))
            
            result = cursor.fetchone()
            if result and result[0]:
                return {
                    'best_val_loss': result[0],
                    'best_epoch': result[1]
                }
            return {'best_val_loss': 0, 'best_epoch': 0}
    
    def _get_alerts_summary(self, training_id: int) -> Dict[str, Any]:
        """Obtiene resumen de alertas para un entrenamiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN level = 'critical' THEN 1 END) as critical,
                    COUNT(CASE WHEN level = 'warning' THEN 1 END) as warning,
                    COUNT(CASE WHEN type LIKE '%overfitting%' THEN 1 END) > 0 as overfitting,
                    COUNT(CASE WHEN type LIKE '%underfitting%' THEN 1 END) > 0 as underfitting
                FROM alerts
                WHERE training_id = ?
            ''', (training_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'total_alerts': result[0],
                    'critical_alerts': result[1],
                    'warning_alerts': result[2],
                    'overfitting_detected': bool(result[3]),
                    'underfitting_detected': bool(result[4])
                }
            return {
                'total_alerts': 0, 'critical_alerts': 0, 'warning_alerts': 0,
                'overfitting_detected': False, 'underfitting_detected': False
            }
    
    def _get_total_epochs(self, training_id: int) -> int:
        """Obtiene el número total de épocas de un entrenamiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(epoch) FROM epoch_metrics WHERE training_id = ?', (training_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0