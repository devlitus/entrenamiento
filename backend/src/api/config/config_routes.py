"""
Rutas REST para configuraci?n avanzada del sistema de entrenamiento.

Este m?dulo define los endpoints REST para la gesti?n de configuraciones,
delegando la l?gica de negocio al ConfigService usando Flask-RESTX.
"""

from flask import request
from flask_restx import Namespace, Resource
import logging
from .config_service import ConfigService
from .config_models import create_config_models

logger = logging.getLogger(__name__)

def create_config_namespace(api, config_service: ConfigService = None):
    """Crea y configura el namespace de configuración."""
    
    if config_service is None:
        config_service = ConfigService()
    
    # Crear modelos
    models = create_config_models(api)
    
    # Crear namespace
    config_ns = Namespace('config', description='Operaciones de configuraci?n del sistema')
    
    @config_ns.route('')
    class ConfigResource(Resource):
        @config_ns.doc('get_config')
        @config_ns.marshal_with(models['config_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def get(self):
            """Obtiene la configuraci?n completa del sistema."""
            try:
                result = config_service.get_full_config()
                return result, 200
            except Exception as e:
                logger.error(f"Error obteniendo configuraci?n: {e}")
                config_ns.abort(500, error=str(e))
        
        @config_ns.doc('update_config')
        @config_ns.expect(models['config_model'])
        @config_ns.marshal_with(models['config_model'])
        @config_ns.response(400, 'Configuraci?n inv?lida', models['error_response_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def put(self):
            """Actualiza la configuraci?n completa del sistema."""
            try:
                new_config = request.get_json()
                if not new_config:
                    config_ns.abort(400, error='Configuraci?n requerida')
                
                result = config_service.update_full_config(new_config)
                return result, 200
            except ValueError as e:
                config_ns.abort(400, error=str(e))
            except Exception as e:
                logger.error(f"Error actualizando configuraci?n: {e}")
                config_ns.abort(500, error=str(e))
    
    @config_ns.route('/section/<string:section_name>')
    class ConfigSectionResource(Resource):
        @config_ns.doc('get_config_section')
        @config_ns.marshal_with(models['config_section_model'])
        @config_ns.response(404, 'Secci?n no encontrada', models['error_response_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def get(self, section_name):
            """Obtiene una secci?n espec?fica de la configuraci?n."""
            try:
                result = config_service.get_config_section(section_name)
                return {'section_name': section_name, 'config': result}, 200
            except ValueError as e:
                config_ns.abort(404, error=str(e))
            except Exception as e:
                logger.error(f"Error obteniendo secci?n {section_name}: {e}")
                config_ns.abort(500, error=str(e))
        
        @config_ns.doc('update_config_section')
        @config_ns.expect(models['config_section_model'])
        @config_ns.marshal_with(models['config_section_model'])
        @config_ns.response(400, 'Configuraci?n inv?lida', models['error_response_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def put(self, section_name):
            """Actualiza una secci?n espec?fica de la configuraci?n."""
            try:
                section_config = request.get_json()
                if not section_config:
                    config_ns.abort(400, error='Configuraci?n de secci?n requerida')
                
                result = config_service.update_config_section(section_name, section_config)
                return {'section_name': section_name, 'config': result}, 200
            except ValueError as e:
                config_ns.abort(400, error=str(e))
            except Exception as e:
                logger.error(f"Error actualizando secci?n {section_name}: {e}")
                config_ns.abort(500, error=str(e))
    
    @config_ns.route('/reset')
    class ConfigResetResource(Resource):
        @config_ns.doc('reset_config')
        @config_ns.marshal_with(models['config_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def post(self):
            """Resetea la configuración a valores por defecto."""
            try:
                result = config_service.reset_config()
                return result, 200
            except Exception as e:
                logger.error(f"Error reseteando configuración: {e}")
                config_ns.abort(500, error=str(e))
    
    @config_ns.route('/validate')
    class ConfigValidateResource(Resource):
        @config_ns.doc('validate_config')
        @config_ns.expect(models['config_model'])
        @config_ns.marshal_with(models['config_validation_model'])
        @config_ns.response(500, 'Error interno', models['error_response_model'])
        def post(self):
            """Valida una configuración proporcionada."""
            try:
                config_to_validate = request.get_json()
                if not config_to_validate:
                    config_ns.abort(400, error='Configuración requerida para validación')
                
                result = config_service.validate_config(config_to_validate)
                return result, 200
            except Exception as e:
                logger.error(f"Error validando configuración: {e}")
                config_ns.abort(500, error=str(e))
    
    @config_ns.route('/health')
    class ConfigHealthResource(Resource):
        @config_ns.doc('config_health_check')
        @config_ns.marshal_with(models['health_response_model'])
        @config_ns.response(500, 'Servicio no disponible', models['error_response_model'])
        def get(self):
            """Verifica el estado del servicio de configuración."""
            try:
                config_data = config_service.get_full_config()
                return {
                    'status': 'healthy',
                    'service': 'config',
                    'timestamp': config_data.get('timestamp', '')
                }, 200
            except Exception as e:
                logger.error(f"Error en health check: {e}")
                return {
                    'status': 'unhealthy',
                    'error': str(e)
                }, 500
    
    return config_ns


def create_config_blueprint(config_service: ConfigService = None):
    """Función de compatibilidad hacia atrás para Blueprint."""
    from flask import Blueprint
    
    if config_service is None:
        config_service = ConfigService()
    
    config_bp = Blueprint('advanced_config', __name__, url_prefix='/api/config')
    
    # Implementación básica para compatibilidad
    @config_bp.route('', methods=['GET'])
    def get_config():
        from flask import jsonify
        try:
            result = config_service.get_full_config()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error obteniendo configuración: {e}")
            return jsonify({'error': str(e)}), 500
    
    return config_bp