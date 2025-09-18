# backend/src/api/predictions/prediction_routes.py
"""
Rutas de predicci?n usando Flask-RESTX para documentaci?n autom?tica.

Endpoints para realizar predicciones con modelos entrenados.
"""

from flask import request, jsonify, Blueprint
from flask_restx import Namespace, Resource
from src.services.predictions.prediction_service import PredictionService

def create_prediction_namespace(models, prediction_service: PredictionService = None):
    """Crea el namespace de prediction con los modelos proporcionados"""
    
    if prediction_service is None:
        prediction_service = PredictionService()
    
    prediction_ns = Namespace('prediction', description='Operaciones de predicci?n de modelos')
    
    # Obtener modelos
    prediction_params_model = models['prediction_params_model']
    prediction_response_model = models['prediction_response_model']
    error_response_model = models['error_response_model']

    @prediction_ns.route('/predict')
    class Prediction(Resource):
        @prediction_ns.expect(prediction_params_model)
        @prediction_ns.marshal_with(prediction_response_model)
        @prediction_ns.response(400, 'Par?metros inv?lidos', error_response_model)
        def post(self):
            """Realiza una predicci?n con el modelo entrenado"""
            try:
                data = request.get_json()
                # L?gica de predicci?n aqu?
                return {
                    'prediction': [0.5, 0.3, 0.2],
                    'confidence': 0.85,
                    'model_used': 'single_layer',
                    'processing_time': 0.001
                }
            except Exception as e:
                return {'error': str(e)}, 400

    return prediction_ns

def create_prediction_blueprint(prediction_service: PredictionService = None) -> Blueprint:
    """Crea blueprint para compatibilidad hacia atr?s"""
    bp = Blueprint('prediction', __name__, url_prefix='/api')
    
    @bp.route('/predict', methods=['POST'])
    def predict():
        """Endpoint de predicci?n b?sico"""
        try:
            data = request.get_json()
            return jsonify({
                'prediction': [0.5, 0.3, 0.2],
                'confidence': 0.85,
                'model_used': 'single_layer',
                'processing_time': 0.001
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return bp