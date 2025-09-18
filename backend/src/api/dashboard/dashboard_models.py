"""
Modelos de datos para endpoints de dashboard usando Flask-RESTX.
"""

from flask_restx import fields

def create_dashboard_models(api):
    """Crea y retorna todos los modelos de dashboard para Flask-RESTX."""
    
    # Modelo para respuesta de overview del dashboard
    dashboard_overview_model = api.model('DashboardOverview', {
        'system_status': fields.String(required=True, description='Estado del sistema', example='active'),
        'timestamp': fields.String(required=True, description='Timestamp de la consulta'),
        'period_days': fields.Integer(required=True, description='Días del período consultado', example=30),
        'total_trainings': fields.Integer(required=True, description='Total de entrenamientos', example=15),
        'active_trainings': fields.Integer(required=True, description='Entrenamientos activos', example=2),
        'completed_trainings': fields.Integer(required=True, description='Entrenamientos completados', example=13),
        'avg_accuracy': fields.Float(required=True, description='Precisión promedio', example=0.85),
        'total_models': fields.Integer(required=True, description='Total de modelos', example=8)
    })
    
    # Modelo para métricas de rendimiento
    performance_metrics_model = api.model('PerformanceMetrics', {
        'cpu_usage': fields.Float(required=True, description='Uso de CPU (%)', example=45.2),
        'memory_usage': fields.Float(required=True, description='Uso de memoria (%)', example=67.8),
        'gpu_usage': fields.Float(required=False, description='Uso de GPU (%)', example=23.1),
        'disk_usage': fields.Float(required=True, description='Uso de disco (%)', example=34.5),
        'network_io': fields.Float(required=True, description='I/O de red (MB/s)', example=12.3)
    })
    
    # Modelo para estadísticas de entrenamiento
    training_stats_model = api.model('TrainingStats', {
        'recent_trainings': fields.Integer(required=True, description='Entrenamientos recientes', example=5),
        'avg_duration': fields.Float(required=True, description='Duración promedio (min)', example=15.7),
        'success_rate': fields.Float(required=True, description='Tasa de éxito (%)', example=92.3),
        'most_used_architecture': fields.String(required=True, description='Arquitectura más usada', example='single_layer')
    })
    
    # Modelo para respuesta de métricas del sistema
    system_metrics_model = api.model('SystemMetrics', {
        'performance': fields.Nested(performance_metrics_model, required=True),
        'training_stats': fields.Nested(training_stats_model, required=True),
        'timestamp': fields.String(required=True, description='Timestamp de las métricas'),
        'uptime': fields.String(required=True, description='Tiempo de actividad', example='2d 14h 32m')
    })
    
    # Modelo para respuesta de actividad reciente
    recent_activity_item_model = api.model('RecentActivityItem', {
        'id': fields.String(required=True, description='ID de la actividad'),
        'type': fields.String(required=True, description='Tipo de actividad', example='training_started'),
        'description': fields.String(required=True, description='Descripción de la actividad'),
        'timestamp': fields.String(required=True, description='Timestamp de la actividad'),
        'status': fields.String(required=True, description='Estado', example='completed')
    })
    
    recent_activity_model = api.model('RecentActivity', {
        'activities': fields.List(fields.Nested(recent_activity_item_model), required=True),
        'total_count': fields.Integer(required=True, description='Total de actividades', example=10)
    })
    
    # Modelo para respuesta de error
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(required=True, description='Mensaje de error')
    })
    
    return {
        'dashboard_overview_model': dashboard_overview_model,
        'performance_metrics_model': performance_metrics_model,
        'training_stats_model': training_stats_model,
        'system_metrics_model': system_metrics_model,
        'recent_activity_item_model': recent_activity_item_model,
        'recent_activity_model': recent_activity_model,
        'error_response_model': error_response_model
    }