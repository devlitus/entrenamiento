"""
Rutas REST para configuraci?n avanzada del sistema de entrenamiento.

Este m?dulo define los endpoints REST para la gesti?n de configuraciones,
delegando la l?gica de negocio al ConfigService.
"""

from flask import Blueprint, request, jsonify
import logging
from .config_service import ConfigService

logger = logging.getLogger(__name__)

def create_config_blueprint(config_service: ConfigService = None) -> Blueprint:
    """Crea y configura el blueprint de configuraci?n."""
    
    if config_service is None:
        config_service = ConfigService()
    
    config_bp = Blueprint('advanced_config', __name__, url_prefix='/api/config')
    
    @config_bp.route('', methods=['GET'])
    def get_config():
        """Obtiene la configuraci?n completa del sistema."""
        try:
            result = config_service.get_full_config()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error obteniendo configuraci?n: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('', methods=['PUT'])
    def update_config():
        """Actualiza la configuraci?n completa del sistema."""
        try:
            new_config = request.get_json()
            if not new_config:
                return jsonify({'error': 'Configuraci?n requerida'}), 400
            
            result = config_service.update_full_config(new_config)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error actualizando configuraci?n: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('/section/<section_name>', methods=['GET'])
    def get_config_section(section_name):
        """Obtiene una secci?n espec?fica de la configuraci?n."""
        try:
            result = config_service.get_config_section(section_name)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            logger.error(f"Error obteniendo secci?n {section_name}: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('/section/<section_name>', methods=['PUT'])
    def update_config_section(section_name):
        """Actualiza una secci?n espec?fica de la configuraci?n."""
        try:
            section_config = request.get_json()
            if not section_config:
                return jsonify({'error': 'Configuraci?n de secci?n requerida'}), 400
            
            result = config_service.update_config_section(section_name, section_config)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error actualizando secci?n {section_name}: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('/reset', methods=['POST'])
    def reset_config():
        """Resetea la configuraci?n a valores por defecto."""
        try:
            result = config_service.reset_config()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error reseteando configuraci?n: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('/validate', methods=['POST'])
    def validate_config():
        """Valida una configuraci?n proporcionada."""
        try:
            config_to_validate = request.get_json()
            if not config_to_validate:
                return jsonify({'error': 'Configuraci?n requerida para validaci?n'}), 400
            
            result = config_service.validate_config(config_to_validate)
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error validando configuraci?n: {e}")
            return jsonify({'error': str(e)}), 500
    
    @config_bp.route('/health', methods=['GET'])
    def health_check():
        """Verifica el estado del servicio de configuraci?n."""
        try:
            return jsonify({
                'status': 'healthy',
                'service': 'config',
                'timestamp': config_service.get_full_config()['timestamp']
            }), 200
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500
    
    return config_bp