# backend/src/api/training_routes.py
"""
Rutas de entrenamiento usando Flask-RESTX para documentación automática.

Endpoints para iniciar, pausar, reanudar y detener entrenamientos.
"""

from flask import request, jsonify
from flask_restx import Namespace, Resource

def create_training_namespace(models):
    """Crea el namespace de training con los modelos proporcionados"""
    
    training_ns = Namespace('training', description='Operaciones de entrenamiento de modelos')
    
    # Obtener modelos
    training_params_model = models['training_params_model']
    training_start_response_model = models['training_start_response_model']
    training_status_response_model = models['training_status_response_model']
    training_control_response_model = models['training_control_response_model']
    error_response_model = models['error_response_model']

    @training_ns.route('/start')
    class TrainingStart(Resource):
        @training_ns.expect(training_params_model)
        @training_ns.marshal_with(training_start_response_model)
        @training_ns.response(400, 'Parámetros inválidos', error_response_model)
        def post(self):
            """Inicia un nuevo entrenamiento"""
            try:
                data = request.get_json()
                # Lógica de entrenamiento aquí
                return {
                    'training_id': 'train_123',
                    'status': 'started',
                    'message': 'Entrenamiento iniciado correctamente',
                    'params': data
                }
            except Exception as e:
                return {'error': str(e)}, 400

    @training_ns.route('/status')
    class TrainingStatus(Resource):
        @training_ns.marshal_with(training_status_response_model)
        def get(self):
            """Obtiene el estado actual del entrenamiento"""
            return {
                'is_training': False,
                'is_paused': False,
                'current_epoch': 0,
                'total_epochs': 0,
                'current_loss': 0.0,
                'training_id': None
            }

    @training_ns.route('/stop')
    class TrainingStop(Resource):
        @training_ns.marshal_with(training_control_response_model)
        def post(self):
            """Detiene el entrenamiento actual"""
            return {
                'status': 'stopped',
                'message': 'Entrenamiento detenido',
                'timestamp': '2024-01-01T00:00:00Z'
            }

    @training_ns.route('/pause')
    class TrainingPause(Resource):
        @training_ns.marshal_with(training_control_response_model)
        def post(self):
            """Pausa el entrenamiento actual"""
            return {
                'status': 'paused',
                'message': 'Entrenamiento pausado',
                'timestamp': '2024-01-01T00:00:00Z'
            }

    @training_ns.route('/resume')
    class TrainingResume(Resource):
        @training_ns.marshal_with(training_control_response_model)
        def post(self):
            """Reanuda el entrenamiento pausado"""
            return {
                'status': 'resumed',
                'message': 'Entrenamiento reanudado',
                'timestamp': '2024-01-01T00:00:00Z'
            }

    return training_ns

# Mantener compatibilidad hacia atrás con blueprints
def create_training_blueprint(training_service):
    """Wrapper para mantener compatibilidad con la función original."""
    from flask import Blueprint
    
    # Crear blueprint tradicional para compatibilidad
    training_bp = Blueprint('training', __name__, url_prefix='/api/training')
    
    # Aquí se podría agregar lógica adicional si es necesaria
    # Por ahora, se recomienda usar create_training_namespace directamente
    
    return training_bp