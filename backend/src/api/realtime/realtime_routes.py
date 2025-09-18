# backend/src/api/realtime_routes.py
"""
Endpoints REST para comunicación en tiempo real usando Flask-RESTX.

Este módulo proporciona endpoints para Server-Sent Events y comunicación
en tiempo real con el frontend.
"""

from flask import Blueprint, Response, request, jsonify
from flask_restx import Namespace, Resource
from datetime import datetime
import json
import time
import uuid
from typing import Dict, Any, Optional, Generator
from utils.logger import setup_logger
from .realtime_models import create_realtime_models

logger = setup_logger(__name__)

def create_realtime_namespace(models, services: Optional[Dict[str, Any]] = None):
    """Crea el namespace de tiempo real con los modelos proporcionados"""
    
    realtime_ns = Namespace('realtime', description='Comunicación en tiempo real')
    
    # Obtener servicios
    realtime_service = services.get('realtime_service') if services else None
    
    # Obtener modelos
    connection_config_model = models['connection_config_model']
    training_progress_model = models['training_progress_model']
    system_event_model = models['system_event_model']
    system_metrics_model = models['system_metrics_model']
    connection_status_model = models['connection_status_model']
    error_response_model = models['error_response_model']
    success_response_model = models['success_response_model']

    def generate_training_events(experiment_id: str) -> Generator[str, None, None]:
        """Genera eventos de progreso de entrenamiento simulados"""
        total_epochs = 100
        
        for epoch in range(1, total_epochs + 1):
            # Simular progreso de entrenamiento
            progress_data = {
                'experiment_id': experiment_id,
                'epoch': epoch,
                'total_epochs': total_epochs,
                'loss': max(0.1, 1.0 - (epoch / total_epochs) * 0.9 + (0.1 * (epoch % 10) / 10)),
                'accuracy': min(0.99, (epoch / total_epochs) * 0.9 + 0.1),
                'val_loss': max(0.15, 1.2 - (epoch / total_epochs) * 0.95),
                'val_accuracy': min(0.95, (epoch / total_epochs) * 0.85 + 0.1),
                'timestamp': datetime.now().isoformat(),
                'status': 'training' if epoch < total_epochs else 'completed'
            }
            
            yield f"data: {json.dumps(progress_data)}\n\n"
            time.sleep(0.5)  # Simular tiempo de entrenamiento
        
        # Evento final
        final_data = {
            'experiment_id': experiment_id,
            'epoch': total_epochs,
            'total_epochs': total_epochs,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'message': 'Entrenamiento completado exitosamente'
        }
        yield f"data: {json.dumps(final_data)}\n\n"

    def generate_system_metrics() -> Generator[str, None, None]:
        """Genera métricas del sistema en tiempo real"""
        import random
        
        while True:
            metrics_data = {
                'cpu_usage': random.uniform(20, 80),
                'memory_usage': random.uniform(30, 90),
                'gpu_usage': random.uniform(0, 100),
                'disk_usage': random.uniform(40, 70),
                'active_experiments': random.randint(0, 5),
                'timestamp': datetime.now().isoformat()
            }
            
            yield f"data: {json.dumps(metrics_data)}\n\n"
            time.sleep(2)  # Actualizar cada 2 segundos

    @realtime_ns.route('/training/<string:experiment_id>')
    class TrainingProgress(Resource):
        @realtime_ns.doc('get_training_progress')
        @realtime_ns.response(200, 'Stream de progreso de entrenamiento')
        @realtime_ns.response(404, 'Experimento no encontrado', error_response_model)
        def get(self, experiment_id):
            """Stream de progreso de entrenamiento en tiempo real"""
            try:
                def event_stream():
                    yield "data: {\"status\": \"connected\", \"experiment_id\": \"" + experiment_id + "\"}\n\n"
                    yield from generate_training_events(experiment_id)
                
                return Response(
                    event_stream(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Access-Control-Allow-Origin': '*'
                    }
                )
            except Exception as e:
                logger.error(f"Error in training progress stream: {e}")
                realtime_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @realtime_ns.route('/metrics')
    class SystemMetrics(Resource):
        @realtime_ns.doc('get_system_metrics')
        @realtime_ns.response(200, 'Stream de métricas del sistema')
        def get(self):
            """Stream de métricas del sistema en tiempo real"""
            try:
                def event_stream():
                    yield "data: {\"status\": \"connected\", \"type\": \"system_metrics\"}\n\n"
                    yield from generate_system_metrics()
                
                return Response(
                    event_stream(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Access-Control-Allow-Origin': '*'
                    }
                )
            except Exception as e:
                logger.error(f"Error in system metrics stream: {e}")
                realtime_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @realtime_ns.route('/events')
    class SystemEvents(Resource):
        @realtime_ns.doc('get_system_events')
        @realtime_ns.response(200, 'Stream de eventos del sistema')
        def get(self):
            """Stream de eventos del sistema en tiempo real"""
            try:
                def event_stream():
                    yield "data: {\"status\": \"connected\", \"type\": \"system_events\"}\n\n"
                    
                    # Generar eventos de ejemplo
                    events = [
                        {'event_type': 'info', 'message': 'Sistema iniciado correctamente'},
                        {'event_type': 'warning', 'message': 'Uso de memoria alto detectado'},
                        {'event_type': 'info', 'message': 'Nuevo experimento iniciado'},
                        {'event_type': 'error', 'message': 'Error en validación de datos'}
                    ]
                    
                    for event in events:
                        event_data = {
                            **event,
                            'timestamp': datetime.now().isoformat(),
                            'source': 'system'
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                        time.sleep(3)
                
                return Response(
                    event_stream(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Access-Control-Allow-Origin': '*'
                    }
                )
            except Exception as e:
                logger.error(f"Error in system events stream: {e}")
                realtime_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @realtime_ns.route('/status')
    class ConnectionStatus(Resource):
        @realtime_ns.doc('get_connection_status')
        @realtime_ns.marshal_with(connection_status_model)
        def get(self):
            """Obtiene el estado de la conexión en tiempo real"""
            try:
                client_id = request.args.get('client_id', str(uuid.uuid4()))
                
                return {
                    'connected': True,
                    'client_id': client_id,
                    'connected_since': datetime.now().isoformat(),
                    'channels': ['training', 'metrics', 'events'],
                    'last_heartbeat': datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Error getting connection status: {e}")
                realtime_ns.abort(500, f"Error interno del servidor: {str(e)}")

    return realtime_ns


def create_realtime_blueprint(services: Optional[Dict[str, Any]] = None) -> Blueprint:
    """
    Crea blueprint para endpoints de tiempo real (compatibilidad hacia atrás).
    
    Args:
        services: Diccionario con servicios inyectados
        
    Returns:
        Blueprint configurado para tiempo real
    """
    bp = Blueprint('realtime', __name__, url_prefix='/api/realtime')
    
    # Obtener servicios
    training_service = services.get('training_service') if services else None
    statistics_service = services.get('statistics_service') if services else None
    
    def create_sse_response(generator: Generator[str, None, None]) -> Response:
        """Crea una respuesta SSE con headers apropiados."""
        response = Response(
            generator,
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Cache-Control'
            }
        )
        return response
    
    @bp.route('/training-progress', methods=['GET'])
    def training_progress_stream():
        """Stream de progreso de entrenamiento en tiempo real."""
        def generate_training_events():
            try:
                # Enviar evento de conexión
                yield f"data: {json.dumps({'status': 'connected', 'message': 'Conectado al stream de entrenamiento'})}\n\n"
                
                # Simular progreso de entrenamiento
                for epoch in range(1, 51):  # 50 épocas
                    training_data = {
                        'epoch': epoch,
                        'total_epochs': 50,
                        'progress': (epoch / 50) * 100,
                        'metrics': {
                            'loss': max(0.01, 0.5 - (epoch * 0.01)),
                            'val_loss': max(0.02, 0.6 - (epoch * 0.008)),
                            'accuracy': min(0.99, 0.7 + (epoch * 0.005)),
                            'val_accuracy': min(0.98, 0.65 + (epoch * 0.004))
                        },
                        'timestamp': datetime.now().isoformat(),
                        'status': 'training'
                    }
                    
                    yield f"data: {json.dumps(training_data)}\n\n"
                    time.sleep(2)
                
                # Evento de finalización
                final_data = {
                    'message': 'Entrenamiento completado exitosamente',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                yield f"data: {json.dumps(final_data)}\n\n"
                
            except Exception as e:
                logger.error(f"Error en stream de entrenamiento: {e}")
                error_data = {
                    'error': f'Error en el stream: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return create_sse_response(generate_training_events())
    
    @bp.route('/system-metrics', methods=['GET'])
    def system_metrics_stream():
        """Stream de métricas del sistema en tiempo real."""
        def generate_system_events():
            try:
                yield f"data: {json.dumps({'status': 'connected', 'message': 'Conectado al stream de métricas'})}\n\n"
                
                import random
                while True:
                    system_data = {
                        'cpu_usage': random.uniform(20, 80),
                        'memory_usage': random.uniform(30, 90),
                        'gpu_usage': random.uniform(0, 100),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    yield f"data: {json.dumps(system_data)}\n\n"
                    time.sleep(5)
                    
            except Exception as e:
                logger.error(f"Error en stream de métricas del sistema: {e}")
                error_data = {
                    'error': f'Error en el stream: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return create_sse_response(generate_system_events())
    
    @bp.route('/status', methods=['GET'])
    def realtime_status():
        """Obtiene el estado de los streams en tiempo real."""
        try:
            status_data = {
                'timestamp': datetime.now().isoformat(),
                'streams': {
                    'training_progress': 'active',
                    'system_metrics': 'active'
                },
                'connections': {
                    'total': 0,
                    'active_streams': 2
                },
                'server_time': datetime.now().isoformat()
            }
            
            return jsonify(status_data), 200
            
        except Exception as e:
            logger.error(f"Error obteniendo estado de tiempo real: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    return bp