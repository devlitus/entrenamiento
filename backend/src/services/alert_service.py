# backend/src/services/alert_service.py

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import time
import json
from dataclasses import dataclass, asdict

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertType(Enum):
    OVERFITTING = "overfitting"
    UNDERFITTING = "underfitting"
    NAN_LOSS = "nan_loss"
    STAGNANT_LEARNING = "stagnant_learning"
    HIGH_RESOURCE_USAGE = "high_resource_usage"
    TEMPERATURE_WARNING = "temperature_warning"
    MEMORY_WARNING = "memory_warning"
    TRAINING_ERROR = "training_error"

@dataclass
class Alert:
    id: str
    type: AlertType
    level: AlertLevel
    title: str
    message: str
    timestamp: float
    data: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False

class AlertService:
    """Servicio de alertas para monitoreo de entrenamiento"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable] = []
        self.thresholds = self._get_default_thresholds()
        self.alert_counter = 0
        
    def _get_default_thresholds(self) -> Dict[str, Any]:
        """Obtiene umbrales por defecto para alertas"""
        return {
            'overfitting': {
                'loss_difference': 0.1,
                'patience_epochs': 5
            },
            'underfitting': {
                'min_improvement': 0.001,
                'patience_epochs': 10
            },
            'stagnant_learning': {
                'min_change': 0.0001,
                'patience_epochs': 15
            },
            'hardware': {
                'cpu_usage': 90.0,
                'memory_usage': 85.0,
                'gpu_usage': 95.0,
                'gpu_memory': 90.0,
                'temperature': 80.0
            }
        }
    
    def set_thresholds(self, thresholds: Dict[str, Any]):
        """Actualiza los umbrales de alerta"""
        self.thresholds.update(thresholds)
    
    def add_callback(self, callback: Callable):
        """Agrega un callback para notificaciones de alertas"""
        self.alert_callbacks.append(callback)
    
    def _generate_alert_id(self) -> str:
        """Genera un ID único para la alerta"""
        self.alert_counter += 1
        return f"alert_{int(time.time())}_{self.alert_counter}"
    
    def _emit_alert(self, alert: Alert):
        """Emite una alerta a todos los callbacks registrados"""
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Error en callback de alerta: {e}")
    
    def create_alert(self, alert_type: AlertType, level: AlertLevel, 
                    title: str, message: str, data: Dict[str, Any] = None) -> Alert:
        """Crea una nueva alerta"""
        alert = Alert(
            id=self._generate_alert_id(),
            type=alert_type,
            level=level,
            title=title,
            message=message,
            timestamp=time.time(),
            data=data or {},
            acknowledged=False,
            resolved=False
        )
        
        self.alerts.append(alert)
        self._emit_alert(alert)
        return alert
    
    def check_overfitting(self, train_loss: List[float], val_loss: List[float]) -> Optional[Alert]:
        """Verifica overfitting y crea alerta si es necesario"""
        if len(train_loss) < 5 or len(val_loss) < 5:
            return None
            
        threshold = self.thresholds['overfitting']['loss_difference']
        patience = self.thresholds['overfitting']['patience_epochs']
        
        # Verificar últimas épocas
        recent_epochs = min(patience, len(train_loss))
        recent_train = train_loss[-recent_epochs:]
        recent_val = val_loss[-recent_epochs:]
        
        # Calcular diferencia promedio
        avg_diff = sum(v - t for v, t in zip(recent_val, recent_train)) / len(recent_val)
        
        if avg_diff > threshold:
            # Verificar si ya existe una alerta similar reciente
            recent_alerts = [a for a in self.alerts[-10:] if a.type == AlertType.OVERFITTING and not a.resolved]
            if recent_alerts:
                return None
                
            return self.create_alert(
                AlertType.OVERFITTING,
                AlertLevel.WARNING,
                "Posible Overfitting Detectado",
                f"La pérdida de validación es {avg_diff:.4f} mayor que la de entrenamiento en promedio",
                {
                    'train_loss': recent_train,
                    'val_loss': recent_val,
                    'difference': avg_diff,
                    'threshold': threshold
                }
            )
        return None
    
    def check_underfitting(self, train_loss: List[float], val_loss: List[float]) -> Optional[Alert]:
        """Verifica underfitting y crea alerta si es necesario"""
        min_epochs = self.thresholds['underfitting']['patience_epochs']
        min_improvement = self.thresholds['underfitting']['min_improvement']
        
        if len(train_loss) < min_epochs:
            return None
            
        # Verificar mejora en las últimas épocas
        recent_train = train_loss[-min_epochs:]
        improvement = recent_train[0] - recent_train[-1]
        
        if improvement < min_improvement:
            recent_alerts = [a for a in self.alerts[-10:] if a.type == AlertType.UNDERFITTING and not a.resolved]
            if recent_alerts:
                return None
                
            return self.create_alert(
                AlertType.UNDERFITTING,
                AlertLevel.WARNING,
                "Posible Underfitting Detectado",
                f"Mejora mínima en {min_epochs} épocas: {improvement:.6f}",
                {
                    'improvement': improvement,
                    'min_improvement': min_improvement,
                    'epochs_checked': min_epochs
                }
            )
        return None
    
    def check_nan_loss(self, loss_value: float) -> Optional[Alert]:
        """Verifica pérdidas NaN o infinitas"""
        if loss_value is None or not isinstance(loss_value, (int, float)):
            return None
            
        if not (loss_value == loss_value):  # NaN check
            return self.create_alert(
                AlertType.NAN_LOSS,
                AlertLevel.CRITICAL,
                "Pérdida NaN Detectada",
                "El modelo ha producido una pérdida NaN, el entrenamiento debe detenerse",
                {'loss_value': 'NaN'}
            )
        
        if abs(loss_value) == float('inf'):
            return self.create_alert(
                AlertType.NAN_LOSS,
                AlertLevel.CRITICAL,
                "Pérdida Infinita Detectada",
                "El modelo ha producido una pérdida infinita, el entrenamiento debe detenerse",
                {'loss_value': 'Infinity' if loss_value > 0 else '-Infinity'}
            )
        
        return None
    
    def check_stagnant_learning(self, loss_history: List[float]) -> Optional[Alert]:
        """Verifica aprendizaje estancado"""
        patience = self.thresholds['stagnant_learning']['patience_epochs']
        min_change = self.thresholds['stagnant_learning']['min_change']
        
        if len(loss_history) < patience:
            return None
            
        recent_losses = loss_history[-patience:]
        max_loss = max(recent_losses)
        min_loss = min(recent_losses)
        change = max_loss - min_loss
        
        if change < min_change:
            recent_alerts = [a for a in self.alerts[-5:] if a.type == AlertType.STAGNANT_LEARNING and not a.resolved]
            if recent_alerts:
                return None
                
            return self.create_alert(
                AlertType.STAGNANT_LEARNING,
                AlertLevel.WARNING,
                "Aprendizaje Estancado",
                f"Cambio mínimo en pérdida durante {patience} épocas: {change:.6f}",
                {
                    'change': change,
                    'min_change': min_change,
                    'epochs_checked': patience
                }
            )
        return None
    
    def check_hardware_alerts(self, hardware_stats: Dict[str, Any]) -> List[Alert]:
        """Verifica alertas relacionadas con hardware"""
        alerts = []
        thresholds = self.thresholds['hardware']
        
        # CPU
        cpu_usage = hardware_stats.get('cpu', {}).get('usage_percent', 0)
        if cpu_usage > thresholds['cpu_usage']:
            alerts.append(self.create_alert(
                AlertType.HIGH_RESOURCE_USAGE,
                AlertLevel.WARNING,
                "Uso Alto de CPU",
                f"CPU al {cpu_usage:.1f}% (umbral: {thresholds['cpu_usage']}%)",
                {'cpu_usage': cpu_usage, 'threshold': thresholds['cpu_usage']}
            ))
        
        # Memoria
        memory_usage = hardware_stats.get('memory', {}).get('usage_percent', 0)
        if memory_usage > thresholds['memory_usage']:
            alerts.append(self.create_alert(
                AlertType.MEMORY_WARNING,
                AlertLevel.WARNING,
                "Uso Alto de Memoria",
                f"Memoria RAM al {memory_usage:.1f}% (umbral: {thresholds['memory_usage']}%)",
                {'memory_usage': memory_usage, 'threshold': thresholds['memory_usage']}
            ))
        
        # GPU
        gpu_stats = hardware_stats.get('gpu')
        if gpu_stats and gpu_stats.get('available'):
            for i, gpu in enumerate(gpu_stats.get('gpus', [])):
                gpu_usage = gpu.get('usage_percent', 0)
                gpu_memory = gpu.get('memory_usage_percent', 0)
                gpu_temp = gpu.get('temperature_c', 0)
                
                if gpu_usage > thresholds['gpu_usage']:
                    alerts.append(self.create_alert(
                        AlertType.HIGH_RESOURCE_USAGE,
                        AlertLevel.WARNING,
                        f"Uso Alto de GPU {i}",
                        f"GPU {i} al {gpu_usage:.1f}% (umbral: {thresholds['gpu_usage']}%)",
                        {'gpu_id': i, 'gpu_usage': gpu_usage, 'threshold': thresholds['gpu_usage']}
                    ))
                
                if gpu_memory > thresholds['gpu_memory']:
                    alerts.append(self.create_alert(
                        AlertType.MEMORY_WARNING,
                        AlertLevel.WARNING,
                        f"Memoria GPU {i} Alta",
                        f"Memoria GPU {i} al {gpu_memory:.1f}% (umbral: {thresholds['gpu_memory']}%)",
                        {'gpu_id': i, 'gpu_memory': gpu_memory, 'threshold': thresholds['gpu_memory']}
                    ))
                
                if gpu_temp > thresholds['temperature']:
                    alerts.append(self.create_alert(
                        AlertType.TEMPERATURE_WARNING,
                        AlertLevel.ERROR,
                        f"Temperatura GPU {i} Alta",
                        f"GPU {i} a {gpu_temp}°C (umbral: {thresholds['temperature']}°C)",
                        {'gpu_id': i, 'temperature': gpu_temp, 'threshold': thresholds['temperature']}
                    ))
        
        return alerts
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Marca una alerta como reconocida"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Marca una alerta como resuelta"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Obtiene alertas activas (no resueltas)"""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """Obtiene alertas por nivel"""
        return [alert for alert in self.alerts if alert.level == level]
    
    def get_recent_alerts(self, hours: int = 24) -> List[Alert]:
        """Obtiene alertas recientes"""
        cutoff_time = time.time() - (hours * 3600)
        return [alert for alert in self.alerts if alert.timestamp > cutoff_time]
    
    def clear_resolved_alerts(self):
        """Elimina alertas resueltas del historial"""
        self.alerts = [alert for alert in self.alerts if not alert.resolved]
    
    def export_alerts(self, filepath: str):
        """Exporta alertas a archivo JSON"""
        alerts_data = [asdict(alert) for alert in self.alerts]
        # Convertir enums a strings
        for alert_data in alerts_data:
            alert_data['type'] = alert_data['type'].value
            alert_data['level'] = alert_data['level'].value
            
        with open(filepath, 'w') as f:
            json.dump(alerts_data, f, indent=2)
