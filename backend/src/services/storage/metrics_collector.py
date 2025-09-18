# backend/src/services/storage/metrics_collector.py

import json
import sqlite3
import time
from typing import Dict, List, Any, Optional
from .database_manager import DatabaseManager


class MetricsCollector:
    """Recolector de métricas de entrenamiento y hardware"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def store_epoch_metrics(self, training_id: int, epoch: int, metrics: Dict[str, Any]):
        """Almacena métricas de una época específica"""
        with self.db_manager.lock:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                advanced_metrics = {}
                for key, value in metrics.items():
                    if key not in ['loss', 'val_loss', 'mae', 'val_mae']:
                        advanced_metrics[key] = value
                
                cursor.execute('''
                    INSERT INTO epoch_metrics 
                    (training_id, epoch, timestamp, loss, val_loss, mae, val_mae, advanced_metrics)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    training_id, epoch, time.time(),
                    metrics.get('loss'), metrics.get('val_loss'),
                    metrics.get('mae'), metrics.get('val_mae'),
                    json.dumps(advanced_metrics) if advanced_metrics else None
                ))
                conn.commit()
    
    def store_hardware_metrics(self, training_id: Optional[int], hardware_data: Dict[str, Any]):
        """Almacena métricas de hardware"""
        with self.db_manager.lock:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO hardware_metrics 
                    (training_id, timestamp, cpu_usage, memory_usage, gpu_usage, 
                     gpu_memory, temperature, hardware_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    training_id, time.time(),
                    hardware_data.get('cpu_usage'),
                    hardware_data.get('memory_usage'),
                    hardware_data.get('gpu_usage'),
                    hardware_data.get('gpu_memory'),
                    hardware_data.get('temperature'),
                    json.dumps(hardware_data)
                ))
                conn.commit()
    
    def store_alert(self, alert_id: str, training_id: Optional[int], alert_type: str,
                   level: str, title: str, message: str, data: Optional[Dict[str, Any]] = None):
        """Almacena una alerta"""
        with self.db_manager.lock:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO alerts 
                    (id, training_id, type, level, title, message, timestamp, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    alert_id, training_id, alert_type, level, title, message,
                    time.time(), json.dumps(data) if data else None
                ))
                conn.commit()
    
    def get_training_metrics(self, training_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las métricas de un entrenamiento"""
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM epoch_metrics 
                WHERE training_id = ? 
                ORDER BY epoch ASC
            ''', (training_id,))
            
            metrics = []
            for row in cursor.fetchall():
                metric = dict(row)
                if metric['advanced_metrics']:
                    metric['advanced_metrics'] = json.loads(metric['advanced_metrics'])
                metrics.append(metric)
            
            return metrics
    
    def get_hardware_metrics(self, training_id: Optional[int] = None, 
                           hours: int = 24) -> List[Dict[str, Any]]:
        """Obtiene métricas de hardware"""
        cutoff_time = time.time() - (hours * 3600)
        
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if training_id:
                cursor.execute('''
                    SELECT * FROM hardware_metrics 
                    WHERE training_id = ? AND timestamp > ?
                    ORDER BY timestamp ASC
                ''', (training_id, cutoff_time))
            else:
                cursor.execute('''
                    SELECT * FROM hardware_metrics 
                    WHERE timestamp > ?
                    ORDER BY timestamp ASC
                ''', (cutoff_time,))
            
            metrics = []
            for row in cursor.fetchall():
                metric = dict(row)
                if metric['hardware_data']:
                    metric['hardware_data'] = json.loads(metric['hardware_data'])
                metrics.append(metric)
            
            return metrics
    
    def get_alerts(self, training_id: Optional[int] = None, 
                  resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene alertas"""
        with self.db_manager.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM alerts WHERE 1=1'
            params = []
            
            if training_id is not None:
                query += ' AND training_id = ?'
                params.append(training_id)
            
            if resolved is not None:
                query += ' AND resolved = ?'
                params.append(resolved)
            
            query += ' ORDER BY timestamp DESC'
            
            cursor.execute(query, params)
            
            alerts = []
            for row in cursor.fetchall():
                alert = dict(row)
                if alert['data']:
                    alert['data'] = json.loads(alert['data'])
                alerts.append(alert)
            
            return alerts