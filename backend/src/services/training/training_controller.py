# c:/dev/entrenamiento/backend/src/services/training/training_controller.py
"""
Controlador principal para gestionar el estado y flujo de entrenamiento.
"""

import threading
import time
from utils.logger import setup_logger

logger = setup_logger()

class TrainingController:
    """Controlador para manejar el estado y flujo de entrenamiento."""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.is_training = False
        self.is_paused = False
        self.should_stop = False
        self.training_thread = None
        
    def start_training(self, training_executor, params):
        """Inicia un entrenamiento en hilo separado."""
        # Si hay un entrenamiento en curso, lo detenemos primero
        if self.is_training:
            logger.info("Deteniendo entrenamiento anterior...")
            self.stop_training()
            # Esperar un poco para que termine
            time.sleep(1)
            
        self.should_stop = False
        self.is_paused = False
        self.is_training = False  # Reset explícito del estado
        
        self.training_thread = threading.Thread(
            target=training_executor.run_training,
            args=(params, self)
        )
        self.training_thread.daemon = True
        self.training_thread.start()
        
    def pause_training(self):
        """Pausa el entrenamiento actual."""
        if self.is_training and not self.is_paused:
            self.is_paused = True
            self.socketio.emit('training_paused')
            logger.info("Entrenamiento pausado")
        else:
            raise Exception("No hay entrenamiento activo para pausar")
            
    def resume_training(self):
        """Reanuda el entrenamiento pausado."""
        if self.is_training and self.is_paused:
            self.is_paused = False
            logger.info("Entrenamiento reanudado")
        else:
            raise Exception("No hay entrenamiento pausado para reanudar")
            
    def stop_training(self):
        """Detiene el entrenamiento actual."""
        if self.is_training:
            self.should_stop = True
            self.is_paused = False
            self.socketio.emit('training_stopped')
            logger.info("Entrenamiento detenido")
        else:
            logger.warning("No hay entrenamiento activo para detener")
            
    def reset_state(self):
        """Resetea completamente el estado del servicio."""
        self.is_training = False
        self.is_paused = False
        self.should_stop = False
        logger.info("Estado del servicio reseteado")
        
    def set_training_active(self):
        """Marca el entrenamiento como activo."""
        self.is_training = True
        
    def set_training_inactive(self):
        """Marca el entrenamiento como inactivo."""
        self.is_training = False
        self.is_paused = False
        self.should_stop = False
        
    def should_continue_training(self):
        """Verifica si el entrenamiento debe continuar."""
        return not self.should_stop
        
    def wait_if_paused(self):
        """Espera mientras el entrenamiento está pausado."""
        while self.is_paused and not self.should_stop:
            time.sleep(0.5)