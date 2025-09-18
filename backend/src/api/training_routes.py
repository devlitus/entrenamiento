# backend/src/api/training_routes.py
"""
Rutas especializadas para operaciones de entrenamiento.

Este módulo contiene todas las rutas relacionadas con el entrenamiento
de modelos, extraídas del routes.py monolítico.
"""

from flask import Blueprint, jsonify, request
from utils.logger import setup_logger

logger = setup_logger()

def create_training_blueprint(training_service):
    """Crea un blueprint para rutas de entrenamiento con el servicio correspondiente.
    
    Args:
        training_service: Instancia del servicio de entrenamiento
        
    Returns:
        Blueprint configurado para entrenamiento
    """
    
    # Crear blueprint único para cada instancia
    training_bp = Blueprint('training', __name__, url_prefix='/api/training')
    
    @training_bp.route('/start', methods=['POST'])
    def start_training():
        """Inicia un nuevo entrenamiento."""
        try:
            params = request.get_json()
            if not params:
                return jsonify({'error': 'Parámetros requeridos'}), 400
            
            result = training_service.start_training(params)
            logger.info(f"Entrenamiento iniciado: {result}")
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Error iniciando entrenamiento: {e}")
            return jsonify({'error': str(e)}), 500
    
    @training_bp.route('/stop', methods=['POST'])
    def stop_training():
        """Detiene el entrenamiento actual."""
        try:
            training_service.stop_training()
            return jsonify({'status': 'stopped'}), 200
            
        except Exception as e:
            logger.error(f"Error deteniendo entrenamiento: {e}")
            return jsonify({'error': str(e)}), 500
    
    @training_bp.route('/pause', methods=['POST'])
    def pause_training():
        """Pausa el entrenamiento actual."""
        try:
            training_service.pause_training()
            return jsonify({'status': 'paused'}), 200
            
        except Exception as e:
            logger.error(f"Error pausando entrenamiento: {e}")
            return jsonify({'error': str(e)}), 500
    
    @training_bp.route('/resume', methods=['POST'])
    def resume_training():
        """Reanuda el entrenamiento pausado."""
        try:
            training_service.resume_training()
            return jsonify({'status': 'resumed'}), 200
            
        except Exception as e:
            logger.error(f"Error reanudando entrenamiento: {e}")
            return jsonify({'error': str(e)}), 500
    
    @training_bp.route('/status', methods=['GET'])
    def get_training_status():
        """Obtiene el estado actual del entrenamiento."""
        try:
            status = {
                'is_training': training_service.is_training,
                'is_paused': training_service.is_paused
            }
            return jsonify(status), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo estado: {e}")
            return jsonify({'error': str(e)}), 500
    
    return training_bp