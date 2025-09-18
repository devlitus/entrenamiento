#!/usr/bin/env python3
"""
Servidor principal del sistema de métricas y monitoreo ML.
Arquitectura limpia y modular.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from src.routes import register_all_routes
from src.services.training.training_controller import TrainingController
from src.services.training.training_executor import TrainingExecutor
from utils.logger import setup_logger

def create_app():
    """Factory para crear la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configurar SocketIO con parámetros específicos
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",
        async_mode='threading',
        logger=True,
        engineio_logger=True,
        ping_timeout=60,
        ping_interval=25
    )
    
    # Configurar logging
    logger = setup_logger()
    app.logger = logger
    
    # Inicializar controlador y ejecutor de entrenamiento
    training_controller = TrainingController(socketio)
    training_executor = TrainingExecutor(socketio)
    
    # Registrar rutas consolidadas
    register_all_routes(app, socketio, training_controller, training_executor)
    
    # Crear directorios necesarios
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    
    return app, socketio

if __name__ == '__main__':
    from src import create_app
    app, socketio = create_app()
    
    print("🚀 Sistema de Métricas ML iniciado")
    print(f"📊 API: http://localhost:{Config.PORT}/api/")
    print(f"📈 Dashboard: http://localhost:5173")
    
    socketio.run(
        app, 
        debug=Config.DEBUG, 
        port=Config.PORT, 
        host=Config.HOST
    )
