# backend/src/api/template_endpoints.py
"""
Endpoints REST para el servicio de gestión de plantillas de modelos.
"""

from flask import Blueprint, request, jsonify
from src.services.templates.template_service import TemplateService
from src.services.validation.model_validation_service import ModelValidationService
from src.schemas.model_schemas import ModelArchitectureSchema, TrainingParamsSchema
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
template_bp = Blueprint('templates', __name__, url_prefix='/api/templates')

# Instancias de servicios
template_service = TemplateService()
validation_service = ModelValidationService()

@template_bp.route('', methods=['GET'])
def list_templates():
    """Lista todas las plantillas disponibles."""
    try:
        # Parámetros de filtrado
        category = request.args.get('category')
        complexity = request.args.get('complexity')
        use_case = request.args.get('use_case')
        
        # Construir filtros
        filters = {}
        if category:
            filters['category'] = category
        if complexity:
            filters['complexity'] = complexity
        if use_case:
            filters['use_case'] = use_case
        
        # Obtener plantillas
        templates = template_service.list_templates(filters=filters)
        
        return jsonify({
            'templates': templates,
            'total_count': len(templates)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/<template_id>', methods=['GET'])
def get_template(template_id):
    """Obtiene una plantilla específica."""
    try:
        template = template_service.get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify(template), 200
        
    except Exception as e:
        logger.error(f"Error getting template {template_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/<template_id>/customize', methods=['POST'])
def customize_template(template_id):
    """Personaliza una plantilla con parámetros específicos."""
    try:
        # Verificar que la plantilla existe
        template = template_service.get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        data = request.get_json() or {}
        customizations = data.get('customizations', {})
        
        # Personalizar plantilla
        customized = template_service.customize_template(template_id, customizations)
        
        # Validar configuración personalizada
        validation_result = validation_service.validate_experiment_config(customized)
        
        response = {
            'customized_template': customized,
            'validation': {
                'valid': validation_result.is_valid,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error customizing template {template_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/recommend', methods=['POST'])
def recommend_templates():
    """Recomienda plantillas basadas en requerimientos."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No requirements provided'}), 400
        
        requirements = data.get('requirements', {})
        limit = data.get('limit', 5)
        
        # Obtener recomendaciones
        recommendations = template_service.recommend_templates(requirements, limit=limit)
        
        return jsonify({
            'recommendations': recommendations,
            'requirements_used': requirements,
            'total_recommendations': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting template recommendations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/categories', methods=['GET'])
def get_categories():
    """Obtiene las categorías disponibles de plantillas."""
    try:
        categories = template_service.get_categories()
        
        return jsonify({
            'categories': categories,
            'total_categories': len(categories)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/complexity-levels', methods=['GET'])
def get_complexity_levels():
    """Obtiene los niveles de complejidad disponibles."""
    try:
        complexity_levels = [
            {
                'level': 'beginner',
                'description': 'Modelos simples, ideales para empezar',
                'characteristics': ['Pocas capas', 'Configuración básica', 'Fácil de entender']
            },
            {
                'level': 'intermediate',
                'description': 'Modelos con complejidad moderada',
                'characteristics': ['Múltiples capas', 'Regularización', 'Optimizaciones básicas']
            },
            {
                'level': 'advanced',
                'description': 'Modelos complejos para casos específicos',
                'characteristics': ['Arquitecturas sofisticadas', 'Técnicas avanzadas', 'Optimización completa']
            }
        ]
        
        return jsonify({
            'complexity_levels': complexity_levels,
            'total_levels': len(complexity_levels)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting complexity levels: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/use-cases', methods=['GET'])
def get_use_cases():
    """Obtiene los casos de uso disponibles."""
    try:
        use_cases = [
            {
                'name': 'regression',
                'description': 'Predicción de valores continuos',
                'examples': ['Precio de casas', 'Temperatura', 'Ventas']
            },
            {
                'name': 'classification',
                'description': 'Clasificación de categorías',
                'examples': ['Spam detection', 'Diagnóstico médico', 'Reconocimiento de imágenes']
            },
            {
                'name': 'time_series',
                'description': 'Análisis de series temporales',
                'examples': ['Predicción de stock', 'Clima', 'Tráfico web']
            },
            {
                'name': 'anomaly_detection',
                'description': 'Detección de anomalías',
                'examples': ['Fraude', 'Fallos de sistema', 'Outliers']
            }
        ]
        
        return jsonify({
            'use_cases': use_cases,
            'total_use_cases': len(use_cases)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting use cases: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/compare', methods=['POST'])
def compare_templates():
    """Compara múltiples plantillas."""
    try:
        data = request.get_json()
        if not data or 'template_ids' not in data:
            return jsonify({'error': 'No template IDs provided'}), 400
        
        template_ids = data['template_ids']
        if len(template_ids) < 2:
            return jsonify({'error': 'At least 2 templates required for comparison'}), 400
        
        # Comparar plantillas
        comparison = template_service.compare_templates(template_ids)
        
        return jsonify(comparison), 200
        
    except Exception as e:
        logger.error(f"Error comparing templates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/search', methods=['GET'])
def search_templates():
    """Busca plantillas por texto."""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'No search query provided'}), 400
        
        limit = request.args.get('limit', 10, type=int)
        
        # Buscar plantillas
        results = template_service.search_templates(query, limit=limit)
        
        return jsonify({
            'query': query,
            'results': results,
            'total_results': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching templates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/<template_id>/validate', methods=['POST'])
def validate_template(template_id):
    """Valida una plantilla específica."""
    try:
        # Obtener plantilla
        template = template_service.get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Validar plantilla
        validation_result = validation_service.validate_experiment_config(template)
        
        response = {
            'template_id': template_id,
            'template_name': template.get('name', 'Unknown'),
            'validation': {
                'valid': validation_result.is_valid,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions
            }
        }
        
        status_code = 200 if validation_result.is_valid else 400
        return jsonify(response), status_code
        
    except Exception as e:
        logger.error(f"Error validating template {template_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/batch-validate', methods=['POST'])
def batch_validate_templates():
    """Valida múltiples plantillas en lote."""
    try:
        data = request.get_json()
        template_ids = data.get('template_ids', []) if data else []
        
        # Si no se especifican IDs, validar todas
        if not template_ids:
            all_templates = template_service.list_templates()
            template_ids = [t['id'] for t in all_templates]
        
        results = []
        for template_id in template_ids:
            try:
                template = template_service.get_template(template_id)
                if template:
                    validation_result = validation_service.validate_experiment_config(template)
                    results.append({
                        'template_id': template_id,
                        'template_name': template.get('name', 'Unknown'),
                        'valid': validation_result.is_valid,
                        'errors': validation_result.errors,
                        'warnings': validation_result.warnings
                    })
                else:
                    results.append({
                        'template_id': template_id,
                        'template_name': 'Not Found',
                        'valid': False,
                        'errors': ['Template not found'],
                        'warnings': []
                    })
            except Exception as e:
                results.append({
                    'template_id': template_id,
                    'template_name': 'Error',
                    'valid': False,
                    'errors': [f'Validation error: {str(e)}'],
                    'warnings': []
                })
        
        # Resumen
        total_valid = sum(1 for r in results if r['valid'])
        summary = {
            'total_templates': len(results),
            'valid_templates': total_valid,
            'invalid_templates': len(results) - total_valid,
            'success_rate': total_valid / len(results) if results else 0
        }
        
        return jsonify({
            'summary': summary,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch template validation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/stats', methods=['GET'])
def get_template_stats():
    """Obtiene estadísticas de plantillas."""
    try:
        stats = template_service.get_stats()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting template stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@template_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check para el servicio de plantillas."""
    try:
        # Verificar que el servicio funciona obteniendo plantillas
        templates = template_service.list_templates()
        
        return jsonify({
            'status': 'healthy',
            'service': 'templates',
            'total_templates': len(templates),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'templates',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500