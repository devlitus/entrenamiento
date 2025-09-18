# backend/src/api/templates/template_models.py
"""
Modelos de datos para endpoints de templates usando Flask-RESTX.

Define los esquemas de request/response para documentación automática.
"""

from flask_restx import fields

def create_template_models(api):
    """Crea los modelos de datos para templates usando la instancia de Api"""
    
    # Modelo para filtros de plantillas
    template_filters_model = api.model('TemplateFilters', {
        'category': fields.String(required=False, description='Categoría de plantilla', example='regression'),
        'complexity': fields.String(required=False, description='Nivel de complejidad', example='beginner'),
        'use_case': fields.String(required=False, description='Caso de uso', example='time_series')
    })
    
    # Modelo para plantilla básica
    template_model = api.model('Template', {
        'id': fields.String(required=True, description='ID único de la plantilla'),
        'name': fields.String(required=True, description='Nombre de la plantilla'),
        'description': fields.String(required=True, description='Descripción de la plantilla'),
        'category': fields.String(required=True, description='Categoría'),
        'complexity': fields.String(required=True, description='Nivel de complejidad'),
        'use_case': fields.String(required=True, description='Caso de uso'),
        'architecture': fields.Raw(required=True, description='Configuración de arquitectura'),
        'parameters': fields.Raw(required=False, description='Parámetros por defecto'),
        'tags': fields.List(fields.String, required=False, description='Etiquetas')
    })
    
    # Modelo para lista de plantillas
    template_list_response_model = api.model('TemplateListResponse', {
        'templates': fields.List(fields.Nested(template_model), required=True, description='Lista de plantillas'),
        'total': fields.Integer(required=True, description='Total de plantillas'),
        'filtered': fields.Integer(required=False, description='Plantillas después de filtros')
    })
    
    # Modelo para personalización de plantilla
    template_customization_model = api.model('TemplateCustomization', {
        'parameters': fields.Raw(required=True, description='Parámetros personalizados'),
        'architecture_changes': fields.Raw(required=False, description='Cambios en arquitectura'),
        'name': fields.String(required=False, description='Nombre personalizado')
    })
    
    # Modelo para recomendaciones
    template_recommendation_request_model = api.model('TemplateRecommendationRequest', {
        'requirements': fields.Raw(required=True, description='Requisitos del usuario'),
        'preferences': fields.Raw(required=False, description='Preferencias opcionales'),
        'limit': fields.Integer(required=False, description='Límite de recomendaciones', example=5)
    })
    
    template_recommendation_model = api.model('TemplateRecommendation', {
        'template': fields.Nested(template_model, required=True, description='Plantilla recomendada'),
        'score': fields.Float(required=True, description='Puntuación de recomendación'),
        'reasons': fields.List(fields.String, required=False, description='Razones de la recomendación')
    })
    
    template_recommendations_response_model = api.model('TemplateRecommendationsResponse', {
        'recommendations': fields.List(fields.Nested(template_recommendation_model), required=True, description='Lista de recomendaciones'),
        'total_analyzed': fields.Integer(required=True, description='Total de plantillas analizadas')
    })
    
    # Modelo para comparación de plantillas
    template_comparison_request_model = api.model('TemplateComparisonRequest', {
        'template_ids': fields.List(fields.String, required=True, description='IDs de plantillas a comparar'),
        'criteria': fields.List(fields.String, required=False, description='Criterios de comparación')
    })
    
    template_comparison_response_model = api.model('TemplateComparisonResponse', {
        'comparison': fields.Raw(required=True, description='Resultado de la comparación'),
        'summary': fields.Raw(required=True, description='Resumen de diferencias'),
        'recommendations': fields.List(fields.String, required=False, description='Recomendaciones basadas en comparación')
    })
    
    # Modelo para búsqueda de plantillas
    template_search_request_model = api.model('TemplateSearchRequest', {
        'query': fields.String(required=True, description='Consulta de búsqueda'),
        'filters': fields.Nested(template_filters_model, required=False, description='Filtros adicionales'),
        'limit': fields.Integer(required=False, description='Límite de resultados', example=10)
    })
    
    # Modelo para validación de plantilla
    template_validation_response_model = api.model('TemplateValidationResponse', {
        'valid': fields.Boolean(required=True, description='Si la plantilla es válida'),
        'errors': fields.List(fields.String, required=True, description='Lista de errores'),
        'warnings': fields.List(fields.String, required=True, description='Lista de advertencias'),
        'suggestions': fields.List(fields.String, required=False, description='Sugerencias de mejora')
    })
    
    # Modelo para estadísticas de plantillas
    template_stats_response_model = api.model('TemplateStatsResponse', {
        'total_templates': fields.Integer(required=True, description='Total de plantillas'),
        'by_category': fields.Raw(required=True, description='Distribución por categoría'),
        'by_complexity': fields.Raw(required=True, description='Distribución por complejidad'),
        'most_used': fields.List(fields.String, required=False, description='Plantillas más utilizadas'),
        'recent_additions': fields.List(fields.String, required=False, description='Plantillas agregadas recientemente')
    })
    
    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error'),
        'code': fields.String(required=False, description='Código de error'),
        'details': fields.Raw(required=False, description='Detalles adicionales del error')
    })
    
    return {
        'template_filters_model': template_filters_model,
        'template_model': template_model,
        'template_list_response_model': template_list_response_model,
        'template_customization_model': template_customization_model,
        'template_recommendation_request_model': template_recommendation_request_model,
        'template_recommendation_model': template_recommendation_model,
        'template_recommendations_response_model': template_recommendations_response_model,
        'template_comparison_request_model': template_comparison_request_model,
        'template_comparison_response_model': template_comparison_response_model,
        'template_search_request_model': template_search_request_model,
        'template_validation_response_model': template_validation_response_model,
        'template_stats_response_model': template_stats_response_model,
        'error_response_model': error_response_model
    }