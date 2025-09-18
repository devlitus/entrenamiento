# backend/src/services/storage/database_manager.py

import os
import sqlite3
import threading
from typing import Any, Dict


class DatabaseManager:
    """Gestor de base de datos para métricas de entrenamiento"""
    
    def __init__(self, db_path: str = 'data/metrics.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._ensure_db_exists()
        self._create_tables()
    
    def _ensure_db_exists(self):
        """Asegura que el directorio de la base de datos existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _create_tables(self):
        """Crea las tablas necesarias en la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de entrenamientos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trainings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    status TEXT DEFAULT 'running',
                    hyperparameters TEXT,
                    model_type TEXT,
                    final_loss REAL,
                    duration REAL,
                    epochs INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de métricas por época
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS epoch_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    training_id INTEGER NOT NULL,
                    epoch INTEGER NOT NULL,
                    timestamp REAL NOT NULL,
                    loss REAL,
                    val_loss REAL,
                    mae REAL,
                    val_mae REAL,
                    advanced_metrics TEXT,
                    FOREIGN KEY (training_id) REFERENCES trainings (id)
                )
            ''')
            
            # Tabla de métricas de hardware
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hardware_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    training_id INTEGER,
                    timestamp REAL NOT NULL,
                    cpu_usage REAL,
                    memory_usage REAL,
                    gpu_usage REAL,
                    gpu_memory REAL,
                    temperature REAL,
                    hardware_data TEXT,
                    FOREIGN KEY (training_id) REFERENCES trainings (id)
                )
            ''')
            
            # Tabla de alertas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id TEXT PRIMARY KEY,
                    training_id INTEGER,
                    type TEXT NOT NULL,
                    level TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    data TEXT,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    resolved BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (training_id) REFERENCES trainings (id)
                )
            ''')
            
            conn.commit()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def cleanup_old_data(self, days: int = 30):
        """Limpia datos antiguos de la base de datos"""
        import time
        cutoff_time = time.time() - (days * 24 * 3600)
        
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Eliminar entrenamientos antiguos y sus datos relacionados
                cursor.execute('''
                    DELETE FROM alerts 
                    WHERE training_id IN (
                        SELECT id FROM trainings WHERE start_time < ?
                    )
                ''', (cutoff_time,))
                
                cursor.execute('''
                    DELETE FROM hardware_metrics 
                    WHERE training_id IN (
                        SELECT id FROM trainings WHERE start_time < ?
                    )
                ''', (cutoff_time,))
                
                cursor.execute('''
                    DELETE FROM epoch_metrics 
                    WHERE training_id IN (
                        SELECT id FROM trainings WHERE start_time < ?
                    )
                ''', (cutoff_time,))
                
                cursor.execute('DELETE FROM trainings WHERE start_time < ?', (cutoff_time,))
                
                conn.commit()