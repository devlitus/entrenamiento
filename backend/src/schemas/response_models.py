# backend/src/schemas/response_models.py

"""
Modelos de respuesta para las APIs REST del sistema ML.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class ExperimentStatus(Enum):
    """Estados posibles de un experimento."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunStatus(Enum):
    """Estados posibles de una ejecución."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ValidationResult:
    """Resultado de validación de configuración."""
    valid: bool
    errors: List[str]
    warnings: List[str] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.suggestions is None:
            self.suggestions = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class ExperimentResponse:
    """Respuesta para operaciones de experimento."""
    id: str
    name: str
    description: str
    status: ExperimentStatus
    config: Dict[str, Any]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    runs_count: Optional[int] = None
    latest_run: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = asdict(self)
        result['status'] = self.status.value
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result


@dataclass
class RunResponse:
    """Respuesta para operaciones de ejecución."""
    id: str
    experiment_id: str
    status: RunStatus
    config: Dict[str, Any]
    metrics: Optional[Dict[str, float]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None
    error_message: Optional[str] = None
    model_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = asdict(self)
        result['status'] = self.status.value
        if self.started_at:
            result['started_at'] = self.started_at.isoformat()
        if self.completed_at:
            result['completed_at'] = self.completed_at.isoformat()
        return result


@dataclass
class TemplateResponse:
    """Respuesta para operaciones de plantilla."""
    id: str
    name: str
    description: str
    category: str
    complexity: str
    framework: str
    config: Dict[str, Any]
    tags: List[str]
    use_cases: List[str]
    requirements: Dict[str, Any]
    performance_metrics: Optional[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class ComparisonResponse:
    """Respuesta para comparación de experimentos."""
    experiments: List[str]
    metrics: List[str]
    results: Dict[str, Dict[str, float]]
    summary: Dict[str, Any]
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class InsightsResponse:
    """Respuesta para insights de experimento."""
    experiment_id: str
    performance_summary: Dict[str, Any]
    recommendations: List[str]
    issues: List[str]
    strengths: List[str]
    improvement_suggestions: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class HealthCheckResponse:
    """Respuesta para health check de servicios."""
    service: str
    status: str
    timestamp: datetime
    version: str
    dependencies: Dict[str, str]
    metrics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result


@dataclass
class PaginatedResponse:
    """Respuesta paginada genérica."""
    items: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class ErrorResponse:
    """Respuesta de error estándar."""
    error: Dict[str, Any]
    
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.error = {
            'code': code,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {'error': self.error}


@dataclass
class ConfigResponse:
    """Respuesta para operaciones de configuración."""
    config: Dict[str, Any]
    version: str
    last_modified: datetime
    schema_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = asdict(self)
        result['last_modified'] = self.last_modified.isoformat()
        return result


@dataclass
class StatsResponse:
    """Respuesta para estadísticas del sistema."""
    total_experiments: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    avg_training_time: float
    most_used_templates: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


@dataclass
class ExportResponse:
    """Respuesta para exportación de datos."""
    format: str
    size: int
    experiments_count: int
    runs_count: int
    created_at: datetime
    download_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = asdict(self)
        result['created_at'] = self.created_at.isoformat()
        return result


@dataclass
class ImportResponse:
    """Respuesta para importación de datos."""
    imported_experiments: int
    imported_runs: int
    skipped_items: int
    errors: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return asdict(self)


# Funciones de utilidad para crear respuestas
def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Crea una respuesta de éxito estándar."""
    return {
        'success': True,
        'message': message,
        'data': data.to_dict() if hasattr(data, 'to_dict') else data,
        'timestamp': datetime.now().isoformat()
    }


def create_error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Crea una respuesta de error estándar."""
    return ErrorResponse(code, message, details).to_dict()


def create_validation_error_response(errors: List[str], warnings: List[str] = None) -> Dict[str, Any]:
    """Crea una respuesta de error de validación."""
    return create_error_response(
        code="VALIDATION_ERROR",
        message="Validation failed",
        details={
            'errors': errors,
            'warnings': warnings or []
        }
    )


def create_not_found_response(resource: str, resource_id: str) -> Dict[str, Any]:
    """Crea una respuesta de recurso no encontrado."""
    return create_error_response(
        code="NOT_FOUND",
        message=f"{resource} not found",
        details={'resource_id': resource_id}
    )


def create_paginated_response(
    items: List[Any],
    total: int,
    page: int,
    per_page: int
) -> Dict[str, Any]:
    """Crea una respuesta paginada."""
    pages = (total + per_page - 1) // per_page
    
    response = PaginatedResponse(
        items=[item.to_dict() if hasattr(item, 'to_dict') else item for item in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )
    
    return create_success_response(response)


# Constantes para códigos de error comunes
class ErrorCodes:
    """Códigos de error estándar."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    BAD_REQUEST = "BAD_REQUEST"
    CONFLICT = "CONFLICT"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


# Constantes para mensajes de éxito comunes
class SuccessMessages:
    """Mensajes de éxito estándar."""
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"
    RETRIEVED = "Resource retrieved successfully"
    VALIDATED = "Validation completed successfully"
    EXPORTED = "Data exported successfully"
    IMPORTED = "Data imported successfully"