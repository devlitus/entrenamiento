# backend/src/api/prediction_routes.py
"""
Rutas especializadas para operaciones de predicción.

Este módulo contiene todas las rutas relacionadas con predicciones
de modelos, extraídas del routes.py monolítico.
"""

from flask import Blueprint, jsonify, request
import numpy as np
import tensorflow as tf
from config import Config
from utils.logger import setup_logger

logger = setup_logger()

# Blueprint para rutas de predicción
prediction_bp = Blueprint('prediction', __name__, url_prefix='/api')

@prediction_bp.route('/status', methods=['GET'])
def get_status():
    """Obtiene el estado del sistema."""
    try:
        return jsonify({
            'status': 'running',
            'message': 'Sistema de entrenamiento activo',
            'timestamp': tf.timestamp().numpy() if hasattr(tf, 'timestamp') else 'N/A'
        }), 200
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/model/info', methods=['GET'])
def get_model_info():
    """Obtiene información del modelo actual."""
    try:
        return jsonify({
            'model_type': 'Sequential',
            'task': 'Celsius to Fahrenheit conversion',
            'input_shape': [1],
            'output_shape': [1],
            'status': 'ready'
        }), 200
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/predict', methods=['GET'])
def predict_simple():
    """Realiza una predicción simple desde parámetros GET."""
    try:
        celsius = request.args.get('celsius', type=float)
        if celsius is None:
            return jsonify({'error': 'Parameter celsius is required'}), 400
        
        # Predicción simple: F = C * 1.8 + 32
        fahrenheit = celsius * 1.8 + 32
        
        return jsonify({
            'celsius': celsius,
            'fahrenheit': fahrenheit,
            'prediction_type': 'simple_formula'
        }), 200
    except Exception as e:
        logger.error(f"Error in simple prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/training-data', methods=['GET'])
def get_training_data():
    """Obtiene información sobre los datos de entrenamiento."""
    try:
        return jsonify({
            'dataset_size': 100,
            'input_range': [-40, 100],
            'output_range': [-40, 212],
            'data_type': 'celsius_fahrenheit_conversion'
        }), 200
    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/dataset', methods=['GET'])
def get_dataset():
    """Obtiene el dataset actual."""
    try:
        # Generar datos de ejemplo
        celsius_data = np.linspace(-40, 100, 20)
        fahrenheit_data = celsius_data * 1.8 + 32
        
        return jsonify({
            'celsius': celsius_data.tolist(),
            'fahrenheit': fahrenheit_data.tolist(),
            'size': len(celsius_data)
        }), 200
    except Exception as e:
        logger.error(f"Error getting dataset: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/model/architecture', methods=['GET'])
def get_model_architecture():
    """Obtiene la arquitectura del modelo actual."""
    try:
        return jsonify({
            'layers': [
                {'type': 'Dense', 'units': 1, 'activation': 'linear'}
            ],
            'total_params': 2,
            'trainable_params': 2,
            'optimizer': 'adam',
            'loss': 'mean_squared_error'
        }), 200
    except Exception as e:
        logger.error(f"Error getting model architecture: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    """Realiza predicción con el modelo entrenado."""
    try:
        data = request.get_json()
        if not data or 'celsius' not in data:
            return jsonify({'error': 'Valor celsius requerido'}), 400
        
        celsius = float(data['celsius'])
        
        # Cargar modelo
        try:
            model = tf.keras.models.load_model(Config.MODEL_PATH)
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            return jsonify({'error': 'Modelo no encontrado'}), 404
        
        # Normalizar entrada
        celsius_normalized = celsius / 100.0
        
        # Predicción
        prediction = model.predict(np.array([[celsius_normalized]]), verbose=0)
        fahrenheit = float(prediction[0][0] * 180.0 + 32.0)
        
        result = {
            'celsius': celsius,
            'fahrenheit': round(fahrenheit, 2),
            'formula_check': round(celsius * 9/5 + 32, 2)
        }
        
        logger.info(f"Predicción: {celsius}°C -> {fahrenheit}°F")
        return jsonify(result), 200
        
    except ValueError:
        return jsonify({'error': 'Valor celsius inválido'}), 400
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/experiments/predict', methods=['POST'])
def experimental_predict():
    """Predicción experimental con métricas adicionales."""
    try:
        data = request.get_json()
        if not data or 'celsius' not in data:
            return jsonify({'error': 'Valor celsius requerido'}), 400
        
        celsius = float(data['celsius'])
        
        # Cargar modelo
        try:
            model = tf.keras.models.load_model(Config.MODEL_PATH)
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            return jsonify({'error': 'Modelo no encontrado'}), 404
        
        # Normalizar entrada
        celsius_normalized = celsius / 100.0
        
        # Predicción con métricas
        prediction = model.predict(np.array([[celsius_normalized]]), verbose=0)
        fahrenheit_pred = float(prediction[0][0] * 180.0 + 32.0)
        fahrenheit_real = celsius * 9/5 + 32
        
        # Calcular error
        error = abs(fahrenheit_pred - fahrenheit_real)
        error_percentage = (error / fahrenheit_real) * 100 if fahrenheit_real != 0 else 0
        
        result = {
            'input': {
                'celsius': celsius,
                'celsius_normalized': celsius_normalized
            },
            'prediction': {
                'fahrenheit': round(fahrenheit_pred, 4),
                'raw_output': float(prediction[0][0])
            },
            'validation': {
                'formula_result': round(fahrenheit_real, 4),
                'absolute_error': round(error, 4),
                'error_percentage': round(error_percentage, 4)
            },
            'model_info': {
                'layers': len(model.layers),
                'parameters': model.count_params()
            }
        }
        
        logger.info(f"Predicción experimental: {celsius}°C -> {fahrenheit_pred}°F (error: {error:.4f})")
        return jsonify(result), 200
        
    except ValueError:
        return jsonify({'error': 'Valor celsius inválido'}), 400
    except Exception as e:
        logger.error(f"Error en predicción experimental: {e}")
        return jsonify({'error': str(e)}), 500