# backend/src/routes.py
"""
Configuraci?n de rutas principales de la aplicaci?n Flask.

Este m?dulo centraliza el registro de todas las rutas y blueprints
de la aplicaci?n, manteniendo una estructura organizada y modular.
"""

from flask import Blueprint
from utils.logger import setup_logger

# Importar blueprints especializados
from src.api.dashboard.dashboard_routes import create_dashboard_blueprint
from src.api.realtime.realtime_routes import create_realtime_blueprint
from src.api.training.training_routes import create_training_blueprint
from src.api.predictions.prediction_routes import create_prediction_blueprint
from src.api.statistic.statistics_routes import create_statistics_blueprint
# from src.api.model.model_routes import create_model_blueprint  # Comentado - m?dulo no existe
# from src.api.experiments.experiment_routes import create_experiment_blueprint  # Comentado - m?dulo no existe
from src.api.templates.template_routes import create_template_blueprint
from src.api.config.config_routes import create_config_blueprint

# Importar blueprints de API REST
# from src.api.validation import validation_bp  # Comentado - ahora usa Flask-RESTX namespaces

logger = setup_logger()

def register_all_routes(app, services):
    """
    Registra todas las rutas y blueprints en la aplicaci?n Flask.
    
    Args:
        app: Instancia de la aplicaci?n Flask
        services: Diccionario con servicios inyectados
    """
    try:
        # Crear y registrar blueprint de entrenamiento
        training_bp = create_training_blueprint(services.get('training_service'))
        app.register_blueprint(training_bp)
        
        # Crear y registrar blueprint de estad?sticas
        statistics_bp = create_statistics_blueprint(services.get('statistics_service'))
        app.register_blueprint(statistics_bp)
        
        # Crear y registrar blueprint de predicciones
        from src.services.predictions.prediction_service import PredictionService
        prediction_service = PredictionService()
        prediction_bp = create_prediction_blueprint(prediction_service)
        app.register_blueprint(prediction_bp)
        
        # Crear y registrar blueprint de modelo
        # model_bp = create_model_blueprint()  # Comentado - m?dulo no existe
        # app.register_blueprint(model_bp)
        
        # Crear y registrar blueprint de dashboard
        dashboard_bp = create_dashboard_blueprint(services)
        app.register_blueprint(dashboard_bp)
        
        # Crear y registrar blueprint de tiempo real
        realtime_bp = create_realtime_blueprint(services)
        app.register_blueprint(realtime_bp)
        
        # Registrar blueprints de API REST
        # app.register_blueprint(validation_bp)  # Comentado - ahora usa Flask-RESTX namespaces
        # Crear y registrar blueprint de experimentos
        # experiment_service = services.get('experiment_service') if services else None
        # experiment_bp = create_experiment_blueprint(experiment_service)  # Comentado - m?dulo no existe
        # app.register_blueprint(experiment_bp)
        # Crear y registrar blueprint de templates
        template_service = services.get('template_service') if services else None
        template_bp = create_template_blueprint(template_service)
        app.register_blueprint(template_bp)
        # Crear y registrar blueprint de configuraci?n
        config_service = services.get('config_service') if services else None
        config_bp = create_config_blueprint(config_service)
        app.register_blueprint(config_bp)
        
        logger.info("Todas las rutas registradas exitosamente")
        
    except Exception as e:
        logger.error(f"Error registrando rutas: {e}")
        raise

from src.api.websocket_handlers import register_websocket_handlers

def register_websocket_handlers(socketio, services=None):
    """Registra los manejadores WebSocket usando el m?dulo refactorizado.
    
    Args:
        socketio: Instancia de Flask-SocketIO
        services: Servicios (mantenido por compatibilidad)
    """
    from src.api.websocket_handlers import register_websocket_handlers as register_handlers
    register_handlers(socketio)
