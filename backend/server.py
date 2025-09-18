#!/usr/bin/env python3
"""
Servidor principal del sistema de métricas y monitoreo ML.
Arquitectura limpia y modular.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_restx import Api
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
    
    # Configurar Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='Neural Network Training API',
        description='API para entrenamiento y gestión de redes neuronales',
        doc='/api/docs/',
        prefix='/api'
    )
    
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
    
    # Crear modelos de datos usando la instancia de Api
    from src.api.training_models import create_training_models
    from src.api.prediction_models import create_prediction_models
    from src.api.statistics_models import create_statistics_models
    
    training_models = create_training_models(api)
    prediction_models = create_prediction_models(api)
    statistics_models = create_statistics_models(api)
    
    # Registrar namespaces de Flask-RESTX
    from src.api.training_routes import create_training_namespace
    from src.api.predictions.prediction_routes import create_prediction_namespace
    from src.api.statistics_routes import create_statistics_namespace
    
    training_ns = create_training_namespace(training_models)
    prediction_ns = create_prediction_namespace(prediction_models)
    statistics_ns = create_statistics_namespace(statistics_models)
    
    api.add_namespace(training_ns, path='/training')
    api.add_namespace(prediction_ns, path='/')
    api.add_namespace(statistics_ns, path='/statistics')
    
    # Registrar rutas consolidadas (para compatibilidad)
    register_all_routes(app, {
        'training_controller': training_controller,
        'training_executor': training_executor
    })
    
    # Crear directorios necesarios
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    
    print("🚀 Sistema de Métricas ML iniciado")
    print(f"📊 API: http://localhost:{Config.PORT}/api/")
    
    socketio.run(
        app, 
        debug=Config.DEBUG, 
        port=Config.PORT, 
        host=Config.HOST
    )
