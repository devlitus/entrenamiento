"""
Sistema de logging centralizado.
"""

import logging
import sys
from pathlib import Path
from config import Config

def setup_logger(name='ml_metrics', level=logging.INFO):
    """Configura el logger del sistema."""
    
    # Crear directorio de logs
    Config.LOGS_DIR.mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    file_handler = logging.FileHandler(
        Config.LOGS_DIR / 'ml_metrics.log'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
