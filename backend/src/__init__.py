# backend/src/__init__.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import numpy as np

from .routes import register_all_routes, register_websocket_handlers
from .sockets import register_socket_handlers

socketio = SocketIO()

def load_model_and_data():
    """Carga el modelo y datos de entrenamiento."""
    model = None
    
    # Intentar cargar modelo existente
    model_path = 'models/temperature_model.keras'
    if os.path.exists(model_path):
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            model = None
    
    # Generar datos de entrenamiento
    celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
    fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)
    
    training_data = {
        'celsius': celsius.tolist(),
        'fahrenheit': fahrenheit.tolist()
    }
    
    return model, training_data

def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='')
    
    # Configuración de CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Inicializar SocketIO con la app
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context():
        # Cargar modelo y datos y adjuntarlos a la aplicación
        app.model, app.training_data = load_model_and_data()

        # Crear servicios (placeholder - se implementará en siguiente fase)
        services = {
            'training_service': None,  # Se inicializará cuando esté disponible
            'statistics_service': None  # Se inicializará cuando esté disponible
        }

        # Registrar rutas modularizadas
        register_all_routes(app, services)
        
        # Registrar manejadores WebSocket
        register_websocket_handlers(socketio, services)
        register_socket_handlers(socketio)

    # Ruta para servir el frontend
    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    return app, socketio
