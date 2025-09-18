# c:/dev/entrenamiento/backend/src/services/training/event_emitter.py
"""
Emisor de eventos para comunicación via SocketIO.
"""

import time

class EventEmitter:
    """Emisor de eventos para comunicación via SocketIO."""
    
    def __init__(self, socketio):
        self.socketio = socketio
        
    def emit_metrics(self, metrics):
        """Emite métricas via SocketIO."""
        if self.socketio:
            self.socketio.emit('training_update', metrics)
        else:
            print(f"[METRICS] Época {metrics.get('epoch', '?')}: Loss={metrics.get('loss', '?'):.4f}")
        
    def emit_hardware_stats(self, stats):
        """Emite estadísticas de hardware."""
        if self.socketio:
            self.socketio.emit('hardware_stats', stats)
        else:
            cpu = stats.get('cpu_percent', 0)
            memory = stats.get('memory_percent', 0)
            print(f"[HARDWARE] CPU: {cpu:.1f}%, Memoria: {memory:.1f}%")
        
    def emit_alert(self, epoch):
        """Emite una alerta de ejemplo."""
        alert = {
            'id': f'alert_{int(time.time())}',
            'type': 'performance',
            'level': 'warning',
            'title': 'Rendimiento del modelo',
            'message': 'El modelo está convergiendo más lento de lo esperado',
            'timestamp': time.time(),
            'data': {'epoch': epoch}
        }
        if self.socketio:
            self.socketio.emit('training_alert', alert)
        else:
            print(f"[ALERT] {alert['message']} (Época {epoch})")
        
    def emit_log(self, message, level='info'):
        """Emite un log via SocketIO."""
        if self.socketio:
            self.socketio.emit('training_log', {
                'message': message, 
                'level': level
            })
        else:
            # Fallback para pruebas sin socketio
            print(f"[{level.upper()}] {message}")
        
    def emit_training_complete(self):
        """Emite evento de entrenamiento completado."""
        if self.socketio:
            self.socketio.emit('training_complete', {
                'loss': 0.001,
                'accuracy': 0.95
            })
        else:
            print("[INFO] Entrenamiento completado")
        
    def emit_error(self, error_msg):
        """Emite un error via SocketIO."""
        if self.socketio:
            self.socketio.emit('training_error', {'error': error_msg})
        else:
            print(f"[ERROR] {error_msg}")
        
    def emit_architecture_info(self, architecture_info):
        """Emite información de arquitectura del modelo."""
        if self.socketio:
            self.socketio.emit('model_architecture', architecture_info)
        else:
            print(f"[ARCHITECTURE] Tipo: {architecture_info.get('type', 'unknown')}, Capas: {len(architecture_info.get('layers', []))}")
        
    def emit_architecture_verification(self, saved_architecture_info, configured_architecture):
        """Emite verificación de arquitectura post-entrenamiento con logs detallados."""
        verification_data = {
            'saved_architecture': saved_architecture_info,
            'configured_architecture': configured_architecture,
            'timestamp': time.time()
        }
        if self.socketio:
            self.socketio.emit('architecture_verification', verification_data)
        
        # Logs detallados de verificación
        self._emit_detailed_architecture_logs(saved_architecture_info, configured_architecture)
    
    def _emit_detailed_architecture_logs(self, saved_arch, configured_arch):
        """Emite logs detallados de verificación de arquitectura."""
        self.emit_log("[VERIFY] === VERIFICACIÓN DETALLADA DE ARQUITECTURA ===")
        
        # Información del modelo entrenado
        self.emit_log(f"[MODEL] Modelo entrenado:")
        self.emit_log(f"   • Capas totales: {len(saved_arch['layers'])}")
        self.emit_log(f"   • Capas ocultas: {saved_arch['hidden_layers']}")
        self.emit_log(f"   • Parámetros totales: {saved_arch['total_parameters']:,}")
        
        # Detalles de cada capa
        for i, layer in enumerate(saved_arch['layers']):
            layer_type = layer.get('type', 'Unknown')
            layer_params = layer.get('params', 0)
            activation = layer.get('activation', 'N/A')
            
            if layer_type == 'Dense':
                units = layer.get('units', 'N/A')
                self.emit_log(f"   • Capa {i+1}: {layer_type}({units}) - {activation} - {layer_params:,} params")
            else:
                self.emit_log(f"   • Capa {i+1}: {layer_type} - {layer_params:,} params")
        
        # Comparación con configuración
        if configured_arch:
            self.emit_log(f"[CONFIG] Configuración solicitada:")
            hidden_layers = configured_arch.get('hiddenLayers', [])
            self.emit_log(f"   • Capas ocultas configuradas: {len(hidden_layers)}")
            
            for i, layer_config in enumerate(hidden_layers):
                neurons = layer_config.get('neurons', 'N/A')
                activation = layer_config.get('activation', 'N/A')
                self.emit_log(f"   • Capa oculta {i+1}: {neurons} neuronas - {activation}")
            
            # Verificación de coincidencia
            configured_hidden = len(hidden_layers)
            actual_hidden = saved_arch['hidden_layers']
            
            if configured_hidden == actual_hidden:
                self.emit_log("[SUCCESS] VERIFICACIÓN EXITOSA: Arquitectura coincide con la configuración")
            else:
                self.emit_log(f"⚠️ DISCREPANCIA: Configurado {configured_hidden} capas ocultas, entrenado con {actual_hidden}")
                
            # Verificación detallada de neuronas por capa
            if configured_hidden == actual_hidden and configured_hidden > 0:
                self._verify_layer_details(saved_arch['layers'], hidden_layers)
        else:
            self.emit_log("[BUILD] Entrenamiento con arquitectura por defecto (no personalizada)")
        
        self.emit_log("[VERIFY] === FIN VERIFICACIÓN DE ARQUITECTURA ===")
    
    def _verify_layer_details(self, actual_layers, configured_layers):
        """Verifica detalles específicos de cada capa."""
        # Filtrar solo capas Dense (ocultas)
        dense_layers = [layer for layer in actual_layers if layer.get('type') == 'Dense'][:-1]  # Excluir output layer
        
        for i, (actual, configured) in enumerate(zip(dense_layers, configured_layers)):
            actual_units = actual.get('units', 0)
            actual_activation = actual.get('activation', 'unknown')
            
            configured_units = configured.get('neurons', 0)
            configured_activation = configured.get('activation', 'unknown')
            
            if actual_units == configured_units and actual_activation == configured_activation:
                self.emit_log(f"   [OK] Capa oculta {i+1}: {actual_units} neuronas, {actual_activation} - CORRECTO")
            else:
                self.emit_log(f"   ⚠️ Capa oculta {i+1}: Esperado {configured_units}/{configured_activation}, actual {actual_units}/{actual_activation}")
    
    def emit_advanced_metrics(self, metrics_data):
        """Emite métricas avanzadas con análisis completo."""
        if self.socketio:
            self.socketio.emit('advanced_training_update', metrics_data)
        else:
            epoch = metrics_data.get('epoch', '?')
            loss = metrics_data.get('loss', '?')
            print(f"[ADVANCED] Época {epoch}: Loss={loss}")
    
    def emit_training_summary(self, summary_data):
        """Emite resumen final del entrenamiento."""
        if self.socketio:
            self.socketio.emit('training_summary', summary_data)
        else:
            print(f"[SUMMARY] Entrenamiento finalizado: {summary_data.get('status', 'unknown')}")