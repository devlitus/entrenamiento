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
    
    # Inicializar servicio de entrenamiento unificado
    from src.services.training_service import TrainingService
    training_service = TrainingService(socketio)
    
    # Importar y crear modelos de datos para Flask-RESTX
    from src.api.training.training_models import create_training_models
    from src.api.predictions.prediction_models import create_prediction_models
    from src.api.statistic.statistics_models import create_statistics_models
    from src.api.models.model_models import create_model_models
    from src.api.dashboard.dashboard_models import create_dashboard_models
    from src.api.config.config_models import create_config_models
    from src.api.experiments.experiment_models import create_experiment_models
    from src.api.realtime.realtime_models import create_realtime_models
    
    training_models = create_training_models(api)
    prediction_models = create_prediction_models(api)
    statistics_models = create_statistics_models(api)
    model_models = create_model_models(api)
    dashboard_models = create_dashboard_models(api)
    config_models = create_config_models(api)
    experiment_models = create_experiment_models(api)
    realtime_models = create_realtime_models(api)
    
    # Importar y crear modelos de templates
    from src.api.templates.template_models import create_template_models
    from src.api.templates.template_routes import create_template_namespace
    template_models = create_template_models(api)
    
    # Importar y crear modelos de validación
    from src.api.validation.validation_models import create_validation_models
    validation_models = create_validation_models(api)
    
    # Registrar namespaces de Flask-RESTX
    from src.api.training.training_routes import create_training_namespace
    from src.api.predictions.prediction_routes import create_prediction_namespace
    from src.api.statistic.statistics_routes import create_statistics_namespace
    from src.api.models.model_routes import create_model_namespace
    from src.api.dashboard.dashboard_routes import create_dashboard_namespace
    from src.api.config.config_routes import create_config_namespace
    from src.api.experiments.experiment_routes import create_experiment_namespace
    from src.api.realtime.realtime_routes import create_realtime_namespace
    
    # Importar y crear namespaces de validación
    from src.api.validation import (
        create_architecture_validation_namespace,
        create_training_validation_namespace,
        create_experiment_validation_namespace,
        create_batch_validation_namespace
    )
    
    architecture_ns = create_architecture_validation_namespace(validation_models)
    validation_training_ns = create_training_validation_namespace(validation_models)
    experiment_ns = create_experiment_validation_namespace(validation_models)
    batch_ns = create_batch_validation_namespace(validation_models)
    
    training_ns = create_training_namespace(training_models, training_service)
    prediction_ns = create_prediction_namespace(prediction_models)
    statistics_ns = create_statistics_namespace(statistics_models)
    template_ns = create_template_namespace(template_models)
    model_ns = create_model_namespace(model_models)
    dashboard_ns = create_dashboard_namespace(dashboard_models)
    config_ns = create_config_namespace(api)
    experiment_main_ns = create_experiment_namespace(experiment_models)
    realtime_ns = create_realtime_namespace(realtime_models)
    
    api.add_namespace(training_ns, path='/training')
    api.add_namespace(prediction_ns, path='/')
    api.add_namespace(statistics_ns, path='/statistics')
    api.add_namespace(template_ns, path='/templates')
    api.add_namespace(model_ns, path='/models')
    api.add_namespace(dashboard_ns, path='/dashboard')
    api.add_namespace(config_ns, path='/config')
    api.add_namespace(experiment_main_ns, path='/experiments')
    api.add_namespace(realtime_ns, path='/realtime')
    
    # Registrar namespaces de validación
    api.add_namespace(architecture_ns, path='/validation/architecture')
    api.add_namespace(validation_training_ns, path='/validation/training')
    api.add_namespace(experiment_ns, path='/validation/experiment')
    api.add_namespace(batch_ns, path='/validation/batch')
    
    # Registrar rutas consolidadas (para compatibilidad)
    register_all_routes(app, {
        'training_controller': training_controller,
        'training_executor': training_executor
    })
    
    # Registrar manejadores WebSocket
    from src.routes import register_websocket_handlers
    register_websocket_handlers(socketio)
    
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
