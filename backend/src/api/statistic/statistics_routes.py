# backend/src/api/statistics_routes.py
"""
Rutas especializadas para operaciones de estadísticas usando Flask-RESTX.

Este módulo contiene todas las rutas relacionadas con estadísticas
y métricas con documentación automática.
"""

from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields
from utils.logger import setup_logger

logger = setup_logger()

def create_statistics_namespace(models, statistics_service=None) -> Namespace:
    """Crea el namespace de statistics con los modelos proporcionados"""
    
    statistics_ns = Namespace('statistics', description='Operaciones de estadísticas y métricas')
    
    # Obtener modelos
    metrics_response_model = models['metrics_response_model']
    error_response_model = models['error_response_model']

    @statistics_ns.route('/dashboard')
    class Dashboard(Resource):
        @statistics_ns.marshal_with(metrics_response_model)
        @statistics_ns.response(500, 'Error interno', error_response_model)
        def get(self):
            """Obtiene datos del dashboard de estadísticas"""
            try:
                return {
                    'loss': 0.05,
                    'accuracy': 0.95,
                    'epoch': 100,
                    'training_time': 45.2,
                    'validation_loss': 0.08
                }
            except Exception as e:
                return {'error': str(e)}, 500

    return statistics_ns

def create_statistics_blueprint(statistics_service=None) -> Blueprint:
    """Crea blueprint para compatibilidad hacia atrás"""
    bp = Blueprint('statistics', __name__, url_prefix='/api')
    
    @bp.route('/dashboard', methods=['GET'])
    def dashboard():
        """Endpoint de dashboard básico"""
        try:
            return jsonify({
                'total_models': 5,
                'total_predictions': 1250,
                'accuracy': 0.95,
                'last_training': '2024-01-15T10:30:00Z'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return bp