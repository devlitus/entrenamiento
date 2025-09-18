"""
Rutas de predicciones refactorizadas.

Proporciona endpoints para operaciones de predicción usando el servicio.
"""

from flask import Blueprint, jsonify, request
from src.services.predictions.prediction_service import PredictionService


def create_prediction_blueprint(prediction_service: PredictionService = None) -> Blueprint:
    """
    Crea el blueprint de predicciones.
    
    Args:
        prediction_service: Instancia del servicio de predicciones
        
    Returns:
        Blueprint configurado
    """
    if prediction_service is None:
        prediction_service = PredictionService()
    
    bp = Blueprint('prediction', __name__, url_prefix='/api')
    
    @bp.route('/status', methods=['GET'])
    def get_status():
        """Obtiene el estado del sistema."""
        try:
            result = prediction_service.get_system_status()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/model/info', methods=['GET'])
    def get_model_info():
        """Obtiene información del modelo actual."""
        try:
            result = prediction_service.get_model_info()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/predict', methods=['GET'])
    def predict_simple():
        """Realiza una predicción simple desde parámetros GET."""
        try:
            celsius = request.args.get('celsius', type=float)
            if celsius is None:
                return jsonify({'error': 'Parameter celsius is required'}), 400
            
            result = prediction_service.predict_simple(celsius)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/training-data', methods=['GET'])
    def get_training_data():
        """Obtiene los datos de entrenamiento."""
        try:
            result = prediction_service.get_training_data()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/dataset', methods=['GET'])
    def get_dataset():
        """Obtiene información del dataset."""
        try:
            result = prediction_service.get_dataset()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/model/architecture', methods=['GET'])
    def get_model_architecture():
        """Obtiene la arquitectura del modelo."""
        try:
            result = prediction_service.get_model_architecture()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/predict', methods=['POST'])
    def predict():
        """Realiza predicciones desde datos POST."""
        try:
            data = request.get_json()
            if not data or 'data' not in data:
                return jsonify({'error': 'Data field is required'}), 400
            
            input_data = data['data']
            if not isinstance(input_data, list):
                input_data = [input_data]
            
            result = prediction_service.predict_batch(input_data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    @bp.route('/experiments/predict', methods=['POST'])
    def experimental_predict():
        """Realiza predicciones experimentales."""
        try:
            data = request.get_json()
            if not data or 'data' not in data:
                return jsonify({'error': 'Data field is required'}), 400
            
            input_data = data['data']
            model_type = data.get('model_type', 'default')
            
            if not isinstance(input_data, list):
                input_data = [input_data]
            
            result = prediction_service.experimental_predict(input_data, model_type)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    
    return bp