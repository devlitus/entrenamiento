# backend/src/services/statistics/insights_generator.py

import sqlite3
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class InsightsGenerator:
    """Servicio para generar insights automáticos y análisis de hiperparámetros"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def generate_auto_insights(self, since_timestamp: float) -> List[Dict[str, Any]]:
        """Genera insights automáticos basados en los datos"""
        insights = []
        
        # Insight sobre tasa de éxito
        success_rate = self._get_success_rate(since_timestamp)
        if success_rate < 70:
            insights.append({
                'id': f'success_rate_{int(time.time())}',
                'type': 'warning',
                'title': 'Baja Tasa de Éxito',
                'description': f'La tasa de éxito actual es del {success_rate:.1f}%. Considera revisar los hiperparámetros.',
                'confidence': 0.8,
                'data_support': {'sample_size': self._get_training_count(since_timestamp)},
                'actionable_steps': [
                    'Revisar learning rate - podría estar muy alto',
                    'Verificar calidad de los datos de entrenamiento',
                    'Considerar early stopping más conservador'
                ],
                'created_at': datetime.now().isoformat()
            })
        
        # Insight sobre hiperparámetros óptimos
        best_lr = self._find_best_learning_rate(since_timestamp)
        if best_lr:
            insights.append({
                'id': f'optimal_lr_{int(time.time())}',
                'type': 'recommendation',
                'title': 'Learning Rate Óptimo Identificado',
                'description': f'Los entrenamientos con learning rate de {best_lr} muestran mejor rendimiento.',
                'confidence': 0.7,
                'data_support': {'sample_size': self._get_training_count(since_timestamp)},
                'actionable_steps': [
                    f'Usar learning rate de {best_lr} en próximos entrenamientos',
                    'Experimentar con valores cercanos para fine-tuning'
                ],
                'created_at': datetime.now().isoformat()
            })
        
        # Insight sobre patrones de overfitting
        overfitting_rate = self._analyze_overfitting_patterns(since_timestamp)
        if overfitting_rate > 0.3:
            insights.append({
                'id': f'overfitting_pattern_{int(time.time())}',
                'type': 'warning',
                'title': 'Patrón de Overfitting Detectado',
                'description': f'El {overfitting_rate*100:.1f}% de los entrenamientos muestran signos de overfitting.',
                'confidence': 0.75,
                'data_support': {'sample_size': self._get_training_count(since_timestamp)},
                'actionable_steps': [
                    'Implementar regularización más agresiva',
                    'Reducir la complejidad del modelo',
                    'Aumentar el tamaño del dataset de validación'
                ],
                'created_at': datetime.now().isoformat()
            })
        
        return insights
    
    def get_hyperparameter_performance_map(self, since_timestamp: float) -> List[Dict[str, Any]]:
        """Obtiene mapa de rendimiento por hiperparámetros"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    t.hyperparameters,
                    AVG(em.val_loss) as avg_performance,
                    COUNT(DISTINCT t.id) as session_count
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ? AND t.hyperparameters IS NOT NULL
                AND em.epoch = (SELECT MAX(epoch) FROM epoch_metrics em2 WHERE em2.training_id = t.id)
                GROUP BY t.hyperparameters
            ''', (since_timestamp,))
            
            heatmap_data = []
            for row in cursor.fetchall():
                try:
                    hyperparams = json.loads(row[0])
                    heatmap_data.append({
                        'learning_rate': hyperparams.get('learning_rate', 0),
                        'batch_size': hyperparams.get('batch_size', 0),
                        'avg_performance': round(row[1], 6) if row[1] else 0,
                        'session_count': row[2]
                    })
                except (json.JSONDecodeError, TypeError):
                    continue
            
            return heatmap_data
    
    def _get_success_rate(self, since_timestamp: float) -> float:
        """Calcula la tasa de éxito de entrenamientos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
                FROM trainings 
                WHERE start_time >= ?
            ''', (since_timestamp,))
            
            result = cursor.fetchone()
            if result and result[0] > 0:
                return (result[1] / result[0]) * 100
            return 0.0
    
    def _get_training_count(self, since_timestamp: float) -> int:
        """Obtiene el número de entrenamientos desde una fecha"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM trainings WHERE start_time >= ?', (since_timestamp,))
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def _find_best_learning_rate(self, since_timestamp: float) -> Optional[float]:
        """Encuentra el learning rate con mejor rendimiento promedio"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    t.hyperparameters,
                    AVG(em.val_loss) as avg_loss
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ? AND t.hyperparameters IS NOT NULL
                AND t.status = 'completed'
                AND em.epoch = (SELECT MAX(epoch) FROM epoch_metrics em2 WHERE em2.training_id = t.id)
                GROUP BY t.hyperparameters
                HAVING COUNT(DISTINCT t.id) >= 2
                ORDER BY avg_loss ASC
                LIMIT 1
            ''', (since_timestamp,))
            
            result = cursor.fetchone()
            if result:
                try:
                    hyperparams = json.loads(result[0])
                    return hyperparams.get('learning_rate')
                except (json.JSONDecodeError, TypeError):
                    pass
            
            return None
    
    def _analyze_overfitting_patterns(self, since_timestamp: float) -> float:
        """Analiza patrones de overfitting en los entrenamientos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Buscar entrenamientos donde val_loss > train_loss significativamente
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT t.id) as total_sessions,
                    COUNT(DISTINCT CASE 
                        WHEN em.val_loss > em.loss * 1.2 THEN t.id 
                    END) as overfitting_sessions
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ? AND t.status = 'completed'
                AND em.epoch = (SELECT MAX(epoch) FROM epoch_metrics em2 WHERE em2.training_id = t.id)
                AND em.loss IS NOT NULL AND em.val_loss IS NOT NULL
            ''', (since_timestamp,))
            
            result = cursor.fetchone()
            if result and result[0] > 0:
                return result[1] / result[0]
            
            return 0.0