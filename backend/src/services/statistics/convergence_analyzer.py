# backend/src/services/statistics/convergence_analyzer.py

import sqlite3
import json
from typing import Dict, List, Any, Optional

class ConvergenceAnalyzer:
    """Servicio para análisis de convergencia y patrones de entrenamiento"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def analyze_convergence_patterns(self, since_timestamp: float) -> Dict[str, Any]:
        """Analiza patrones de convergencia"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Obtener datos de convergencia
            cursor.execute('''
                SELECT 
                    t.id,
                    COUNT(em.epoch) as total_epochs,
                    MIN(em.val_loss) as best_loss,
                    AVG(em.val_loss) as avg_loss
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.start_time >= ? AND t.status = 'completed'
                GROUP BY t.id
                HAVING COUNT(em.epoch) >= 5
            ''', (since_timestamp,))
            
            convergence_data = []
            for row in cursor.fetchall():
                session_id, total_epochs, best_loss, avg_loss = row
                
                # Estimar época de convergencia
                convergence_epoch = self._estimate_convergence_epoch(session_id)
                
                convergence_data.append({
                    'session_id': session_id,
                    'total_epochs': total_epochs,
                    'convergence_epoch': convergence_epoch,
                    'best_loss': best_loss,
                    'convergence_efficiency': convergence_epoch / total_epochs if convergence_epoch else 0
                })
            
            if not convergence_data:
                return {
                    'avg_convergence': 0,
                    'fastest': 0,
                    'slowest': 0,
                    'efficiency_distribution': {}
                }
            
            convergence_epochs = [d['convergence_epoch'] for d in convergence_data if d['convergence_epoch']]
            
            return {
                'avg_convergence': round(sum(convergence_epochs) / len(convergence_epochs), 1) if convergence_epochs else 0,
                'fastest': min(convergence_epochs) if convergence_epochs else 0,
                'slowest': max(convergence_epochs) if convergence_epochs else 0,
                'efficiency_distribution': self._calculate_efficiency_distribution(convergence_data)
            }
    
    def get_top_performing_sessions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtiene las sesiones con mejor rendimiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT 
                    t.id, t.name, t.start_time, t.end_time, 
                    t.hyperparameters, MIN(em.val_loss) as best_loss
                FROM trainings t
                JOIN epoch_metrics em ON t.id = em.training_id
                WHERE t.status = 'completed' AND em.val_loss IS NOT NULL
                GROUP BY t.id
                ORDER BY best_loss ASC
                LIMIT ?
            ''', (limit,))
            
            top_sessions = []
            for row in cursor.fetchall():
                session_id, name, start_time, end_time, hyperparams_json, best_loss = row
                
                # Obtener métricas adicionales
                convergence_epoch = self._find_convergence_epoch(session_id)
                total_epochs = self._get_total_epochs(session_id)
                
                try:
                    hyperparams = json.loads(hyperparams_json) if hyperparams_json else {}
                except (json.JSONDecodeError, TypeError):
                    hyperparams = {}
                
                duration = int(end_time - start_time) if end_time else None
                
                top_sessions.append({
                    'id': session_id,
                    'name': name or f'Training_{session_id}',
                    'best_loss': round(best_loss, 6),
                    'convergence_epoch': convergence_epoch,
                    'total_epochs': total_epochs,
                    'duration_seconds': duration,
                    'hyperparameters': {
                        'learning_rate': hyperparams.get('learning_rate', 0),
                        'batch_size': hyperparams.get('batch_size', 0),
                        'epochs': hyperparams.get('epochs', 0)
                    },
                    'efficiency_score': round(convergence_epoch / total_epochs, 2) if convergence_epoch and total_epochs else 0
                })
            
            return top_sessions
    
    def _estimate_convergence_epoch(self, training_id: int) -> Optional[int]:
        """Estima la época donde el modelo convergió"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT epoch, val_loss
                FROM epoch_metrics
                WHERE training_id = ? AND val_loss IS NOT NULL
                ORDER BY epoch
            ''', (training_id,))
            
            metrics = cursor.fetchall()
            if len(metrics) < 5:
                return None
            
            # Buscar el punto donde la mejora se vuelve mínima
            best_loss = float('inf')
            convergence_epoch = None
            improvement_threshold = 0.001  # 0.1% de mejora
            
            for i, (epoch, val_loss) in enumerate(metrics):
                if val_loss < best_loss:
                    improvement = (best_loss - val_loss) / best_loss if best_loss != float('inf') else 1
                    best_loss = val_loss
                    
                    # Si la mejora es significativa, actualizar convergencia
                    if improvement > improvement_threshold:
                        convergence_epoch = epoch
                    
                    # Si llevamos varias épocas sin mejora significativa, considerar convergido
                    if i > 5 and convergence_epoch and (epoch - convergence_epoch) > 5:
                        break
            
            return convergence_epoch
    
    def _find_convergence_epoch(self, training_id: int) -> Optional[int]:
        """Encuentra la época donde el modelo convergió (método simplificado)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT epoch
                FROM epoch_metrics
                WHERE training_id = ? AND val_loss = (
                    SELECT MIN(val_loss) FROM epoch_metrics WHERE training_id = ?
                )
                LIMIT 1
            ''', (training_id, training_id))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def _get_total_epochs(self, training_id: int) -> int:
        """Obtiene el número total de épocas de un entrenamiento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(epoch) FROM epoch_metrics WHERE training_id = ?', (training_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0
    
    def _calculate_efficiency_distribution(self, convergence_data: List[Dict]) -> Dict[str, int]:
        """Calcula la distribución de eficiencia de convergencia"""
        if not convergence_data:
            return {'high': 0, 'medium': 0, 'low': 0}
        
        high_efficiency = sum(1 for d in convergence_data if d['convergence_efficiency'] > 0.7)
        medium_efficiency = sum(1 for d in convergence_data if 0.3 <= d['convergence_efficiency'] <= 0.7)
        low_efficiency = len(convergence_data) - high_efficiency - medium_efficiency
        
        return {
            'high': high_efficiency,
            'medium': medium_efficiency,
            'low': low_efficiency
        }