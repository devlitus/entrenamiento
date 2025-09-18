"""
Rutas REST para gestión de plantillas de modelos usando Flask-RESTX.
"""

from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from datetime import datetime
from src.services.validation.model_validation_service import ModelValidationService
from src.services.templates.template_service import TemplateService
from .template_models import create_template_models
import logging

logger = logging.getLogger(__name__)

def create_template_namespace(models, template_service=None):
    """Crea el namespace de templates con los modelos proporcionados"""
    
    if template_service is None:
        template_service = TemplateService()
    
    validation_service = ModelValidationService()
    
    templates_ns = Namespace('templates', description='Gestión de plantillas de modelos')
    
    # Obtener modelos
    template_filters_model = models['template_filters_model']
    template_model = models['template_model']
    template_list_response_model = models['template_list_response_model']
    template_customization_model = models['template_customization_model']
    template_recommendation_request_model = models['template_recommendation_request_model']
    template_recommendations_response_model = models['template_recommendations_response_model']
    template_comparison_request_model = models['template_comparison_request_model']
    template_comparison_response_model = models['template_comparison_response_model']
    template_search_request_model = models['template_search_request_model']
    template_validation_response_model = models['template_validation_response_model']
    template_stats_response_model = models['template_stats_response_model']
    error_response_model = models['error_response_model']

    @templates_ns.route('/')
    class TemplateList(Resource):
        @templates_ns.doc('list_templates')
        @templates_ns.expect(template_filters_model, validate=False)
        @templates_ns.marshal_with(template_list_response_model)
        def get(self):
            """Lista todas las plantillas disponibles con filtros opcionales"""
            try:
                # Obtener parámetros de filtro
                category = request.args.get('category')
                complexity = request.args.get('complexity')
                use_case = request.args.get('use_case')
                
                # Aplicar filtros
                templates = template_service.list_templates(
                    category=category,
                    complexity=complexity,
                    use_case=use_case
                )
                
                return {
                    'templates': templates,
                    'total': len(templates),
                    'filtered': len(templates)
                }
                
            except Exception as e:
                logger.error(f"Error listando plantillas: {e}")
                templates_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @templates_ns.route('/<string:template_id>')
    class Template(Resource):
        @templates_ns.doc('get_template')
        @templates_ns.marshal_with(template_model)
        def get(self, template_id):
            """Obtiene una plantilla específica por ID"""
            try:
                template = template_service.get_template(template_id)
                if not template:
                    templates_ns.abort(404, f"Plantilla {template_id} no encontrada")
                return template
                
            except Exception as e:
                logger.error(f"Error obteniendo plantilla {template_id}: {e}")
                templates_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @templates_ns.route('/<string:template_id>/customize')
    class TemplateCustomize(Resource):
        @templates_ns.doc('customize_template')
        @templates_ns.expect(template_customization_model)
        @templates_ns.marshal_with(template_model)
        def post(self, template_id):
            """Personaliza una plantilla con parámetros específicos"""
            try:
                data = request.get_json()
                if not data:
                    templates_ns.abort(400, "Datos de personalización requeridos")
                
                customized = template_service.customize_template(template_id, data)
                return customized
                
            except Exception as e:
                logger.error(f"Error personalizando plantilla {template_id}: {e}")
                templates_ns.abort(500, f"Error interno del servidor: {str(e)}")

    @templates_ns.route('/recommend')
    class TemplateRecommend(Resource):
        @templates_ns.doc('recommend_templates')
        @templates_ns.expect(template_recommendation_request_model)
        @templates_ns.marshal_with(template_recommendations_response_model)
        def post(self):
            """Recomienda plantillas basadas en requisitos del usuario"""
            try:
                data = request.get_json()
                if not data or 'requirements' not in data:
                    templates_ns.abort(400, "Requisitos son obligatorios")
                
                recommendations = template_service.recommend_templates(
                    data['requirements'],
                    preferences=data.get('preferences'),
                    limit=data.get('limit', 5)
                )
                
                return {
                    'recommendations': recommendations,
                    'total_analyzed': len(template_service.list_templates())
                }
                
            except Exception as e:
                logger.error(f"Error generando recomendaciones: {e}")
                templates_ns.abort(500, f"Error interno del servidor: {str(e)}")

    return templates_ns

def create_template_blueprint(template_service=None):
    """Crea y configura el blueprint de templates (para compatibilidad)."""
    
    if template_service is None:
        template_service = TemplateService()
    
    validation_service = ModelValidationService()
    
    template_bp = Blueprint('templates', __name__, url_prefix='/api/templates')
    
    # Usar servicio proporcionado o crear uno nuevo
    service = template_service or TemplateService()
    
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
            templates = service.list_templates(filters=filters)
            
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
            template = service.get_template(template_id)
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
            template = service.get_template(template_id)
            if not template:
                return jsonify({'error': 'Template not found'}), 404
            
            data = request.get_json() or {}
            customizations = data.get('customizations', {})
            
            # Personalizar plantilla
            customized = service.customize_template(template_id, customizations)
            
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
            data = request.get_json() or {}
            requirements = data.get('requirements', {})
            
            recommendations = service.recommend_templates(requirements)
            
            return jsonify({
                'recommendations': recommendations,
                'total_count': len(recommendations)
            }), 200
            
        except Exception as e:
            logger.error(f"Error recommending templates: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @template_bp.route('/categories', methods=['GET'])
    def get_categories():
        """Obtiene las categorías disponibles."""
        categories = [
            {'id': 'regression', 'name': 'Regresión', 'description': 'Modelos de regresión'},
            {'id': 'classification', 'name': 'Clasificación', 'description': 'Modelos de clasificación'},
            {'id': 'clustering', 'name': 'Clustering', 'description': 'Modelos de agrupamiento'},
            {'id': 'time_series', 'name': 'Series Temporales', 'description': 'Modelos para series temporales'}
        ]
        return jsonify({'categories': categories}), 200

    @template_bp.route('/complexity-levels', methods=['GET'])
    def get_complexity_levels():
        """Obtiene los niveles de complejidad disponibles."""
        levels = [
            {'id': 'basic', 'name': 'Básico', 'description': 'Modelos simples y rápidos'},
            {'id': 'intermediate', 'name': 'Intermedio', 'description': 'Modelos con complejidad moderada'},
            {'id': 'advanced', 'name': 'Avanzado', 'description': 'Modelos complejos y sofisticados'}
        ]
        return jsonify({'complexity_levels': levels}), 200

    @template_bp.route('/use-cases', methods=['GET'])
    def get_use_cases():
        """Obtiene los casos de uso disponibles."""
        use_cases = [
            {'id': 'prediction', 'name': 'Predicción', 'description': 'Predicción de valores'},
            {'id': 'analysis', 'name': 'Análisis', 'description': 'Análisis de datos'},
            {'id': 'optimization', 'name': 'Optimización', 'description': 'Optimización de procesos'},
            {'id': 'research', 'name': 'Investigación', 'description': 'Investigación y experimentación'}
        ]
        return jsonify({'use_cases': use_cases}), 200

    @template_bp.route('/compare', methods=['POST'])
    def compare_templates():
        """Compara múltiples plantillas."""
        try:
            data = request.get_json() or {}
            template_ids = data.get('template_ids', [])
            
            if not template_ids:
                return jsonify({'error': 'No template IDs provided'}), 400
            
            comparison = service.compare_templates(template_ids)
            return jsonify(comparison), 200
            
        except Exception as e:
            logger.error(f"Error comparing templates: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @template_bp.route('/search', methods=['GET'])
    def search_templates():
        """Busca plantillas por texto."""
        try:
            query = request.args.get('q', '').lower()
            if not query:
                return jsonify({'templates': [], 'total_count': 0}), 200
            
            all_templates = service.list_templates()
            matching_templates = []
            
            for template in all_templates:
                # Buscar en nombre, descripción y categoría
                searchable_text = f"{template.get('name', '')} {template.get('description', '')} {template.get('category', '')}".lower()
                if query in searchable_text:
                    matching_templates.append(template)
            
            return jsonify({
                'templates': matching_templates,
                'total_count': len(matching_templates),
                'query': query
            }), 200
            
        except Exception as e:
            logger.error(f"Error searching templates: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @template_bp.route('/<template_id>/validate', methods=['POST'])
    def validate_template(template_id):
        """Valida una plantilla específica."""
        try:
            template = service.get_template(template_id)
            if not template:
                return jsonify({'error': 'Template not found'}), 404
            
            validation_result = validation_service.validate_experiment_config(template)
            
            return jsonify({
                'template_id': template_id,
                'validation': {
                    'valid': validation_result.is_valid,
                    'errors': validation_result.errors,
                    'warnings': validation_result.warnings,
                    'suggestions': validation_result.suggestions
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error validating template {template_id}: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @template_bp.route('/stats', methods=['GET'])
    def get_template_stats():
        """Obtiene estadísticas de las plantillas."""
        try:
            templates = service.list_templates()
            
            stats = {
                'total_templates': len(templates),
                'by_category': {},
                'by_complexity': {},
                'by_use_case': {}
            }
            
            for template in templates:
                # Estadísticas por categoría
                category = template.get('category', 'unknown')
                stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                
                # Estadísticas por complejidad
                complexity = template.get('complexity', 'unknown')
                stats['by_complexity'][complexity] = stats['by_complexity'].get(complexity, 0) + 1
                
                # Estadísticas por caso de uso
                use_case = template.get('use_case', 'unknown')
                stats['by_use_case'][use_case] = stats['by_use_case'].get(use_case, 0) + 1
            
            return jsonify(stats), 200
            
        except Exception as e:
            logger.error(f"Error getting template stats: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @template_bp.route('/health', methods=['GET'])
    def health_check():
        """Verifica el estado del servicio de plantillas."""
        try:
            templates_count = len(service.list_templates())
            return jsonify({
                'status': 'healthy',
                'templates_available': templates_count,
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    return template_bp