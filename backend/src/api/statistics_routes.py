# backend/src/api/statistics_routes.py
"""
Rutas especializadas para operaciones de estadísticas.

Este módulo contiene todas las rutas relacionadas con estadísticas
y métricas, extraídas del routes.py monolítico.
"""

from flask import Blueprint, jsonify, request
from utils.logger import setup_logger

logger = setup_logger()

def create_statistics_blueprint(statistics_service):
    """Crea un blueprint para rutas de estadísticas con el servicio correspondiente.
    
    Args:
        statistics_service: Instancia del servicio de estadísticas
        
    Returns:
        Blueprint configurado para estadísticas
    """
    
    # Crear blueprint único para cada instancia
    statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')
    
    @statistics_bp.route('/dashboard', methods=['GET'])
    def get_dashboard_data():
        """Obtiene datos del dashboard."""
        try:
            data = statistics_service.get_dashboard_data()
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo datos dashboard: {e}")
            return jsonify({'error': str(e)}), 500
    
    @statistics_bp.route('/trends', methods=['GET'])
    def get_trends():
        """Obtiene análisis de tendencias."""
        try:
            data = statistics_service.get_trend_analysis()
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo tendencias: {e}")
            return jsonify({'error': str(e)}), 500
    
    @statistics_bp.route('/efficiency', methods=['GET'])
    def get_efficiency_metrics():
        """Obtiene métricas de eficiencia."""
        try:
            data = statistics_service.get_efficiency_metrics()
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo eficiencia: {e}")
            return jsonify({'error': str(e)}), 500
    
    @statistics_bp.route('/insights', methods=['GET'])
    def get_auto_insights():
        """Obtiene insights automáticos."""
        try:
            data = statistics_service.generate_auto_insights()
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo insights: {e}")
            return jsonify({'error': str(e)}), 500
    
    @statistics_bp.route('/hyperparameters', methods=['GET'])
    def get_hyperparameter_performance():
        """Obtiene mapa de rendimiento de hiperparámetros."""
        try:
            data = statistics_service.get_hyperparameter_performance_map()
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo hiperparámetros: {e}")
            return jsonify({'error': str(e)}), 500
    
    @statistics_bp.route('/training-data', methods=['GET'])
    def get_training_data():
        """Obtiene datos de entrenamiento."""
        try:
            limit = request.args.get('limit', 100, type=int)
            data = statistics_service.get_training_data(limit=limit)
            return jsonify(data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de entrenamiento: {e}")
            return jsonify({'error': str(e)}), 500
    
    return statistics_bp