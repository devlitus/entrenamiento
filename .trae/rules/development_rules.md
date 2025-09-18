# Reglas de Desarrollo - Neural Network Trainer

## REGLAS CRÍTICAS - NUNCA VIOLAR

### 1. PRESERVACIÓN DE FUNCIONALIDADES EXISTENTES
- **NUNCA** modificar funciones existentes sin verificar todas sus dependencias
- **NUNCA** cambiar signatures de funciones públicas sin migración completa
- **NUNCA** eliminar endpoints o rutas sin deprecación previa
- **NUNCA** modificar el formato de eventos WebSocket existentes
- **SIEMPRE** mantener compatibilidad hacia atrás

### 2. ARQUITECTURA MODULAR ESTRICTA
- **Backend**: Servicios independientes en `src/services/`
- **Frontend**: Componentes atómicos en `src/components/`
- **Comunicación**: Solo a través de interfaces definidas
- **Estado**: Zustand stores separados por dominio
- **Configuración**: Centralizada en `config.py`

### 3. LÍMITES DE CÓDIGO
- **Máximo 100 líneas por archivo** - Si excede, refactorizar en módulos
- **Máximo 20 líneas por función** - Dividir en funciones más pequeñas
- **Máximo 5 parámetros por función** - Usar objetos de configuración
- **Máximo 3 niveles de anidación** - Extraer lógica compleja

## PATRONES OBLIGATORIOS

### Backend (Python)
```python
# ✅ CORRECTO - Servicio modular
class TrainingService:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger()
    
    def execute_training(self, params: TrainingParams) -> TrainingResult:
        # Lógica específica del servicio
        pass

# ❌ INCORRECTO - Función monolítica
def train_model_with_everything(lr, epochs, data, arch, callbacks, ...):
    # 200+ líneas de código mezclado
    pass
```

### Frontend (TypeScript)
```typescript
// ✅ CORRECTO - Hook personalizado
export function useTrainingState() {
  const { training, startTraining } = useTrainingStore();
  return { training, startTraining };
}

// ✅ CORRECTO - Componente atómico
interface TrainingButtonProps {
  onStart: () => void;
  disabled: boolean;
}

export function TrainingButton({ onStart, disabled }: TrainingButtonProps) {
  return <button onClick={onStart} disabled={disabled}>Entrenar</button>;
}

// ❌ INCORRECTO - Componente monolítico
export function TrainingDashboard() {
  // 150+ líneas mezclando lógica, estado y UI
}
```

## REGLAS DE MODIFICACIÓN

### Antes de Modificar Código Existente
1. **Identificar dependencias**: Buscar todas las referencias
2. **Verificar tests**: Ejecutar tests relacionados
3. **Revisar interfaces**: Confirmar contratos públicos
4. **Planificar migración**: Si hay breaking changes

### Al Agregar Nuevas Funcionalidades
1. **Crear nuevo servicio/componente**: No modificar existentes
2. **Definir interfaces claras**: Contratos bien definidos
3. **Implementar tests**: Cobertura mínima 80%
4. **Documentar cambios**: En `docs/` si es necesario

### Al Refactorizar
1. **Mantener funcionalidad**: Comportamiento idéntico
2. **Migrar gradualmente**: Paso a paso, no todo a la vez
3. **Verificar integración**: Tests end-to-end
4. **Actualizar documentación**: Solo si cambian interfaces

## ESTRUCTURA DE SERVICIOS OBLIGATORIA

### Backend Services
```
src/services/
├── training/
│   ├── __init__.py
│   ├── training_executor.py      # Ejecutor principal
│   ├── model_builder.py          # Constructor de modelos
│   ├── data_generator.py         # Generación de datos
│   └── callbacks.py              # Callbacks personalizados
├── monitoring/
│   ├── hardware_monitor.py       # Monitoreo de hardware
│   ├── metrics_calculator.py     # Cálculo de métricas
│   └── alert_service.py          # Sistema de alertas
└── storage/
    ├── metrics_storage.py        # Persistencia de métricas
    └── model_storage.py          # Persistencia de modelos
```

### Frontend Components
```
src/components/
├── common/                       # Componentes reutilizables
├── training/                     # Específicos de entrenamiento
├── monitoring/                   # Monitoreo y métricas
├── architecture/                 # Visualización de arquitectura
└── dashboard/                    # Dashboard principal
```

## COMUNICACIÓN ENTRE CAPAS

### API REST - Solo para CRUD
```python
# ✅ CORRECTO
@api_bp.route('/model/architecture', methods=['POST'])
def set_model_architecture():
    # Validación + delegación a servicio
    return service.configure_architecture(data)
```

### WebSockets - Solo para Streaming
```python
# ✅ CORRECTO
@socketio.on('start_training')
def handle_start_training(data):
    # Validación + delegación a servicio
    training_service.start_training(data)
```

### Frontend - Solo UI y Estado
```typescript
// ✅ CORRECTO
export function TrainingPage() {
  const { startTraining } = useTrainingService();
  const { config } = useArchitectureStore();
  
  return <TrainingForm onSubmit={startTraining} config={config} />;
}
```

## TESTING OBLIGATORIO

### Backend
- **Unit tests**: Cada servicio individual
- **Integration tests**: Comunicación entre servicios
- **API tests**: Endpoints REST y WebSocket

### Frontend
- **Component tests**: Renderizado y interacciones
- **Hook tests**: Lógica de estado
- **Integration tests**: Flujos completos

## VALIDACIÓN ANTES DE COMMIT

### Checklist Obligatorio
- [ ] Tests pasan al 100%
- [ ] No hay funcionalidades rotas
- [ ] Límites de líneas respetados
- [ ] Interfaces públicas intactas
- [ ] Documentación actualizada (si aplica)
- [ ] Logs apropiados agregados
- [ ] Configuración centralizada

### Comandos de Verificación
```bash
# Backend
cd backend && python -m pytest
cd backend && python verify_architecture.py

# Frontend
cd frontend && npm test
cd frontend && npm run build
```

## MANEJO DE ERRORES ESTÁNDAR

### Backend
```python
try:
    result = service.execute_operation(params)
    logger.info(f"Operación exitosa: {result}")
    return jsonify(result), 200
except ValidationError as e:
    logger.warning(f"Error de validación: {e}")
    return jsonify({'error': str(e)}), 400
except Exception as e:
    logger.error(f"Error interno: {e}")
    return jsonify({'error': 'Error interno del servidor'}), 500
```

### Frontend
```typescript
try {
  const result = await api.executeOperation(params);
  toast.success('Operación exitosa');
  return result;
} catch (error) {
  console.error('Error en operación:', error);
  toast.error('Error en la operación');
  throw error;
}
```

---

**IMPORTANTE**: Estas reglas son OBLIGATORIAS. Cualquier violación puede romper el sistema completo. Siempre verificar antes de hacer cambios.