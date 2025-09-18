# backend/src/services/hardware_monitor.py

import psutil
import time
from typing import Dict, Optional
import threading
import json

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

class HardwareMonitor:
    """Monitor de recursos de hardware del sistema"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.current_stats = {}
        self.history = []
        self.max_history = 100  # Mantener últimas 100 mediciones
        
    def get_cpu_stats(self) -> Dict[str, float]:
        """Obtiene estadísticas de CPU"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_freq = psutil.cpu_freq()
        
        stats = {
            'usage_percent': cpu_percent,
            'frequency_mhz': cpu_freq.current if cpu_freq else 0,
            'core_count': psutil.cpu_count(),
            'core_count_logical': psutil.cpu_count(logical=True)
        }
        
        # CPU por núcleo
        per_cpu = psutil.cpu_percent(percpu=True, interval=0.1)
        stats['per_core_usage'] = per_cpu
        
        return stats
    
    def get_memory_stats(self) -> Dict[str, float]:
        """Obtiene estadísticas de memoria RAM"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': memory.total / (1024**3),
            'available_gb': memory.available / (1024**3),
            'used_gb': memory.used / (1024**3),
            'usage_percent': memory.percent,
            'swap_total_gb': swap.total / (1024**3),
            'swap_used_gb': swap.used / (1024**3),
            'swap_percent': swap.percent
        }
    
    def get_gpu_stats(self) -> Optional[Dict]:
        """Obtiene estadísticas de GPU si está disponible"""
        if not GPU_AVAILABLE:
            return None
            
        try:
            gpus = GPUtil.getGPUs()
            if not gpus:
                return None
                
            gpu_stats = []
            for gpu in gpus:
                stats = {
                    'id': gpu.id,
                    'name': gpu.name,
                    'usage_percent': gpu.load * 100,
                    'memory_total_mb': gpu.memoryTotal,
                    'memory_used_mb': gpu.memoryUsed,
                    'memory_free_mb': gpu.memoryFree,
                    'memory_usage_percent': (gpu.memoryUsed / gpu.memoryTotal) * 100 if gpu.memoryTotal > 0 else 0,
                    'temperature_c': gpu.temperature
                }
                gpu_stats.append(stats)
                
            return {
                'available': True,
                'count': len(gpu_stats),
                'gpus': gpu_stats
            }
        except Exception as e:
            return {
                'available': False,
                'error': str(e)
            }
    
    def get_disk_stats(self) -> Dict[str, float]:
        """Obtiene estadísticas de disco"""
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        stats = {
            'total_gb': disk_usage.total / (1024**3),
            'used_gb': disk_usage.used / (1024**3),
            'free_gb': disk_usage.free / (1024**3),
            'usage_percent': (disk_usage.used / disk_usage.total) * 100
        }
        
        if disk_io:
            stats.update({
                'read_bytes': disk_io.read_bytes,
                'write_bytes': disk_io.write_bytes,
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count
            })
            
        return stats
    
    def get_network_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de red"""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def get_temperature_stats(self) -> Optional[Dict]:
        """Obtiene temperaturas del sistema si están disponibles"""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
                
            temp_stats = {}
            for name, entries in temps.items():
                temp_stats[name] = []
                for entry in entries:
                    temp_stats[name].append({
                        'label': entry.label or 'Unknown',
                        'current': entry.current,
                        'high': entry.high,
                        'critical': entry.critical
                    })
            return temp_stats
        except (AttributeError, OSError):
            # No disponible en todos los sistemas
            return None
    
    def get_complete_stats(self) -> Dict:
        """Obtiene todas las estadísticas del sistema"""
        timestamp = time.time()
        
        stats = {
            'timestamp': timestamp,
            'cpu': self.get_cpu_stats(),
            'memory': self.get_memory_stats(),
            'gpu': self.get_gpu_stats(),
            'disk': self.get_disk_stats(),
            'network': self.get_network_stats(),
            'temperature': self.get_temperature_stats()
        }
        
        # Calcular métricas derivadas
        stats['system_load'] = {
            'cpu_memory_avg': (stats['cpu']['usage_percent'] + stats['memory']['usage_percent']) / 2,
            'overall_health': self._calculate_health_score(stats)
        }
        
        return stats
    
    def _calculate_health_score(self, stats: Dict) -> float:
        """Calcula un puntaje de salud del sistema (0-100)"""
        score = 100.0
        
        # Penalizar por uso alto de CPU
        if stats['cpu']['usage_percent'] > 90:
            score -= 30
        elif stats['cpu']['usage_percent'] > 70:
            score -= 15
            
        # Penalizar por uso alto de memoria
        if stats['memory']['usage_percent'] > 90:
            score -= 30
        elif stats['memory']['usage_percent'] > 80:
            score -= 15
            
        # Penalizar por uso alto de GPU
        gpu_stats = stats.get('gpu')
        if gpu_stats and gpu_stats.get('available'):
            for gpu in gpu_stats.get('gpus', []):
                if gpu['usage_percent'] > 95:
                    score -= 20
                elif gpu['usage_percent'] > 85:
                    score -= 10
                    
                if gpu['memory_usage_percent'] > 95:
                    score -= 20
                elif gpu['memory_usage_percent'] > 85:
                    score -= 10
        
        return max(0.0, score)
    
    def start_monitoring(self, interval: float = 1.0, callback=None):
        """Inicia el monitoreo continuo"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval, callback),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Detiene el monitoreo continuo"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def _monitor_loop(self, interval: float, callback):
        """Loop principal de monitoreo"""
        while self.monitoring:
            try:
                stats = self.get_complete_stats()
                self.current_stats = stats
                
                # Agregar al historial
                self.history.append(stats)
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                
                # Llamar callback si se proporciona
                if callback:
                    callback(stats)
                    
                time.sleep(interval)
            except Exception as e:
                print(f"Error en monitoreo de hardware: {e}")
                time.sleep(interval)
    
    def get_current_stats(self) -> Dict:
        """Obtiene las estadísticas actuales"""
        if not self.current_stats:
            return self.get_complete_stats()
        return self.current_stats
    
    def get_history(self, last_n: Optional[int] = None) -> list:
        """Obtiene el historial de estadísticas"""
        if last_n:
            return self.history[-last_n:]
        return self.history
    
    def export_stats(self, filepath: str):
        """Exporta estadísticas a archivo JSON"""
        data = {
            'current': self.current_stats,
            'history': self.history
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
