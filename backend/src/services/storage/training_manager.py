# backend/src/services/storage/training_manager.py

import json
import sqlite3
import time
from typing import Dict, List, Any, Optional
from .database_manager import DatabaseManager


class TrainingManager:
    """Gestor de sesiones de entrenamiento"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_training_session(self, name: str, hyperparameters: Dict[str, Any], 
                               model_type: str = 'regression') -> int:
        """Crea una nueva sesión de entrenamiento"""
        with self.db_manager.lock:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO trainings (name, start_time, hyperparameters, model_type)
                    VALUES (?, ?, ?, ?)
                ''', (name, time.time(), json.dumps(hyperparameters), model_type))
                training_id = cursor.lastrowid
                conn.commit()
                return training_id
    
    def update_training_status(self, training_id: int, status: str, 
                              final_loss: Optional[float] = None, 
                              epochs: Optional[int] = None):
        """Actualiza el estado de un entrenamiento"""
        with self.db_manager.lock:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                end_time = time.time() if status in ['completed', 'failed'] else None
                duration = None
                
                if end_time:
                    cursor.execute('SELECT start_time FROM trainings WHERE id = ?', (training_id,))
                    result = cursor.fetchone()
                    if result:
                        duration = end_time - result[0]
                
                cursor.execute('''
                    UPDATE trainings 
                    SET status = ?, end_time = ?, final_loss = ?, duration = ?, epochs = ?
                    WHERE id = ?
                ''', (status, end_time, final_loss, duration, epochs, training_id))
                conn.commit()
    
    def get_training_sessions_with_filters(self, days: int = 30, status: Optional[str] = None, 
                                         limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene sesiones de entrenamiento con filtros"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM trainings WHERE start_time > ?'
            params = [cutoff_time]
            
            if status:
                query += ' AND status = ?'
                params.append(status)
            
            query += ' ORDER BY start_time DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            
            sessions = []
            for row in cursor.fetchall():
                session = dict(row)
                if session['hyperparameters']:
                    session['hyperparameters'] = json.loads(session['hyperparameters'])
                sessions.append(session)
            
            return sessions
    
    def get_training_summary(self, training_id: int) -> Dict[str, Any]:
        """Obtiene un resumen completo de un entrenamiento"""
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM trainings WHERE id = ?', (training_id,))
            training = cursor.fetchone()
            
            if not training:
                return {}
            
            summary = dict(training)
            if summary['hyperparameters']:
                summary['hyperparameters'] = json.loads(summary['hyperparameters'])
            
            return summary
    
    def export_training_data(self, training_id: int, filepath: str):
        """Exporta todos los datos de un entrenamiento a JSON"""
        summary = self.get_training_summary(training_id)
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)