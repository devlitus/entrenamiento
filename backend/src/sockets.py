# backend/src/sockets.py

"""Manejadores de eventos SocketIO para el entrenamiento.
Versión moderna que usa TrainingExecutor en lugar de train_model legacy.
"""

from flask_socketio import emit
from src.services.training.training_executor import TrainingExecutor
from src.services.training.training_controller import TrainingController

# Instancias globales
training_controller = None

def register_socket_handlers(socketio):
    """Registra los manejadores de eventos SocketIO."""
    
    global training_controller
    
    # Crear instancias con socketio
    from src.services.training.training_controller import TrainingController
    training_controller = TrainingController(socketio)
    training_executor = TrainingExecutor(socketio)
    
    @socketio.on('start_training')
    def handle_start_training(data):
        """Maneja el inicio del entrenamiento usando el sistema moderno."""
        try:
            emit('training_log', {
                'message': '🚀 Iniciando entrenamiento con sistema moderno...',
                'level': 'info'
            })
            
            # Usar TrainingExecutor en lugar de train_model legacy
            socketio.start_background_task(
                training_executor.run_training, data, training_controller
            )
            
        except Exception as e:
            emit('training_error', {'error': f'Error iniciando entrenamiento: {str(e)}'})
    
    @socketio.on('stop_training')
    def handle_stop_training():
        """Maneja la detención del entrenamiento."""
        try:
            training_controller.stop_training()
            emit('training_log', {
                'message': '⏹️ Entrenamiento detenido por el usuario',
                'level': 'warning'
            })
        except Exception as e:
            emit('training_error', {'error': f'Error deteniendo entrenamiento: {str(e)}'})
    
    @socketio.on('pause_training')
    def handle_pause_training():
        """Maneja la pausa del entrenamiento."""
        try:
            training_controller.pause_training()
            emit('training_log', {
                'message': '⏸️ Entrenamiento pausado',
                'level': 'info'
            })
        except Exception as e:
            emit('training_error', {'error': f'Error pausando entrenamiento: {str(e)}'})
    
    @socketio.on('resume_training')
    def handle_resume_training():
        """Maneja la reanudación del entrenamiento."""
        try:
            training_controller.resume_training()
            emit('training_log', {
                'message': '▶️ Entrenamiento reanudado',
                'level': 'info'
            })
        except Exception as e:
            emit('training_error', {'error': f'Error reanudando entrenamiento: {str(e)}'})
    
    @socketio.on('get_training_status')
    def handle_get_training_status():
        """Obtiene el estado actual del entrenamiento."""
        try:
            status = training_controller.get_status()
            emit('training_status', status)
        except Exception as e:
            emit('training_error', {'error': f'Error obteniendo estado: {str(e)}'})
