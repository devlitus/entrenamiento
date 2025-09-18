"""
Configuración centralizada del sistema.
"""

import os
from pathlib import Path

class Config:
    """Configuración principal del sistema."""
    
    # Configuración del servidor
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Directorios
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    MODELS_DIR = BASE_DIR / 'models'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Rutas de archivos
    MODEL_PATH = MODELS_DIR / 'temperature_model.keras'
    TRAINING_DATA_PATH = DATA_DIR / 'training_results.json'
    
    # Configuración de entrenamiento
    DEFAULT_EPOCHS = 20
    DEFAULT_BATCH_SIZE = 32
    DEFAULT_LEARNING_RATE = 0.01
    
    # Configuración de monitoreo
    HARDWARE_MONITOR_INTERVAL = 2.0
    METRICS_BUFFER_SIZE = 100
    MAX_ALERTS = 50
