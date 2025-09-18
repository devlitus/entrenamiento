# backend/src/api/websocket_handlers.py
"""
Manejadores de eventos WebSocket para el entrenamiento.

Este módulo contiene los manejadores WebSocket optimizados siguiendo
los estándares de código y patrones establecidos.
"""

from flask_socketio import emit
from src.services.training.training_executor import TrainingExecutor
from src.services.training.training_controller import TrainingController
import logging

logger = logging.getLogger(__name__)

# Instancia global del controlador
training_controller = None

def register_websocket_handlers(socketio):
    """Registra los manejadores de eventos WebSocket.
    
    Args:
        socketio: Instancia de Flask-SocketIO configurada
        
    Note:
        Inicializa el controlador de entrenamiento y registra todos
        los eventos WebSocket necesarios para la comunicación en tiempo real.
    """
    global training_controller
    
    # Inicializar servicios
    training_controller = TrainingController(socketio)
    training_executor = TrainingExecutor(socketio)
    
    @socketio.on('start_training')
    def handle_start_training(data):
        """Inicia el entrenamiento con validación de datos."""
        try:
            if not data:
                emit('training_error', {'error': 'Datos de entrenamiento requeridos'})
                return
                
            _emit_log('🚀 Iniciando entrenamiento con sistema moderno...', 'info')
            
            # Ejecutar entrenamiento en background
            socketio.start_background_task(
                training_executor.run_training, data, training_controller
            )
            
        except Exception as e:
            logger.error(f"Error iniciando entrenamiento: {str(e)}")
            emit('training_error', {'error': f'Error iniciando entrenamiento: {str(e)}'})
    
    @socketio.on('stop_training')
    def handle_stop_training():
        """Detiene el entrenamiento actual."""
        try:
            training_controller.stop_training()
            _emit_log('⏹️ Entrenamiento detenido por el usuario', 'warning')
            
        except Exception as e:
            logger.error(f"Error deteniendo entrenamiento: {str(e)}")
            emit('training_error', {'error': f'Error deteniendo entrenamiento: {str(e)}'})
    
    @socketio.on('pause_training')
    def handle_pause_training():
        """Pausa el entrenamiento actual."""
        try:
            training_controller.pause_training()
            _emit_log('⏸️ Entrenamiento pausado', 'info')
            
        except Exception as e:
            logger.error(f"Error pausando entrenamiento: {str(e)}")
            emit('training_error', {'error': f'Error pausando entrenamiento: {str(e)}'})
    
    @socketio.on('resume_training')
    def handle_resume_training():
        """Reanuda el entrenamiento pausado."""
        try:
            training_controller.resume_training()
            _emit_log('▶️ Entrenamiento reanudado', 'info')
            
        except Exception as e:
            logger.error(f"Error reanudando entrenamiento: {str(e)}")
            emit('training_error', {'error': f'Error reanudando entrenamiento: {str(e)}'})
    
    @socketio.on('get_training_status')
    def handle_get_training_status():
        """Obtiene el estado actual del entrenamiento."""
        try:
            status = training_controller.get_status()
            emit('training_status', status)
            
        except Exception as e:
            logger.error(f"Error obteniendo estado: {str(e)}")
            emit('training_error', {'error': f'Error obteniendo estado: {str(e)}'})

def _emit_log(message, level='info'):
    """Función auxiliar para emitir logs de entrenamiento.
    
    Args:
        message (str): Mensaje a emitir
        level (str): Nivel del log ('info', 'warning', 'error')
    """
    emit('training_log', {'message': message, 'level': level})