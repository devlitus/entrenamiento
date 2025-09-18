# Reglas de Flujo de Trabajo - Neural Network Trainer

## FLUJO OBLIGATORIO PARA NUEVAS FEATURES

### 1. ANÁLISIS PREVIO (OBLIGATORIO)
```bash
# Antes de cualquier cambio, ejecutar:
1. Identificar archivos afectados
2. Buscar dependencias existentes
3. Verificar tests relacionados
4. Revisar interfaces públicas
```

### 2. PLANIFICACIÓN (OBLIGATORIO)
- **Crear plan detallado** en `docs/` si la feature es compleja
- **Identificar breaking changes** potenciales
- **Definir estrategia de migración** si es necesario
- **Estimar impacto** en funcionalidades existentes

### 3. IMPLEMENTACIÓN INCREMENTAL
- **Paso 1**: Crear nuevos servicios/componentes (NO modificar existentes)
- **Paso 2**: Implementar interfaces y contratos
- **Paso 3**: Agregar tests unitarios
- **Paso 4**: Integrar gradualmente
- **Paso 5**: Tests de integración

### 4. VALIDACIÓN COMPLETA
```bash
# Backend
cd backend
python -m pytest -v
python verify_architecture.py
python run_complete_test.py

# Frontend  
cd frontend
npm test
npm run build
npm run type-check
```

## REGLAS DE REFACTORING

### ANTES DE REFACTORIZAR
1. **Documentar comportamiento actual**: Tests que capturen el comportamiento
2. **Identificar todas las dependencias**: Buscar referencias en todo el proyecto
3. **Crear tests de regresión**: Para verificar que nada se rompe
4. **Planificar en pasos pequeños**: Refactoring incremental

### DURANTE EL REFACTORING
1. **Un cambio a la vez**: No mezclar refactoring con nuevas features
2. **Mantener tests verdes**: Nunca commitear con tests rotos
3. **Verificar funcionalidad**: Probar manualmente después de cada paso
4. **Documentar cambios**: En commits descriptivos

### DESPUÉS DEL REFACTORING
1. **Ejecutar suite completa de tests**
2. **Verificar performance**: No degradar rendimiento
3. **Actualizar documentación**: Si cambiaron interfaces
4. **Code review**: Revisión por otro desarrollador

## PATRONES DE COMMIT OBLIGATORIOS

### Estructura de Commits
```
tipo(scope): descripción breve

Descripción detallada del cambio y por qué fue necesario.

- Cambio específico 1
- Cambio específico 2
- Impacto en funcionalidades existentes

Fixes: #issue-number (si aplica)
```

### Tipos de Commit
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **refactor**: Refactoring sin cambio de funcionalidad
- **test**: Agregar o modificar tests
- **docs**: Cambios en documentación
- **style**: Cambios de formato (no afectan funcionalidad)
- **perf**: Mejoras de performance
- **chore**: Tareas de mantenimiento

### Ejemplos
```bash
feat(training): agregar soporte para arquitecturas multi-layer

Implementa configuración dinámica de capas ocultas para modelos
de redes neuronales, manteniendo compatibilidad con arquitectura
por defecto.

- Nuevo endpoint /api/model/architecture
- Validación de configuración de capas
- Integración con ModelBuilder existente
- Tests unitarios y de integración

Fixes: #123
```

## REGLAS DE TESTING OBLIGATORIAS

### Coverage Mínimo
- **Backend**: 80% coverage mínimo
- **Frontend**: 70% coverage mínimo
- **Servicios críticos**: 90% coverage mínimo

### Tipos de Tests Requeridos
```python
# Backend - Estructura obligatoria
tests/
├── unit/
│   ├── services/
│   ├── routes/
│   └── utils/
├── integration/
│   ├── api/
│   └── websocket/
└── e2e/
    └── training_flow/
```

```typescript
// Frontend - Estructura obligatoria
src/
├── components/
│   └── __tests__/
├── hooks/
│   └── __tests__/
├── services/
│   └── __tests__/
└── stores/
    └── __tests__/
```

### Tests Obligatorios para Cada Feature
1. **Unit tests**: Lógica aislada
2. **Integration tests**: Comunicación entre módulos
3. **API tests**: Endpoints REST y WebSocket
4. **Component tests**: Renderizado y interacciones
5. **E2E tests**: Flujo completo de usuario

## MANEJO DE DEPENDENCIAS

### Backend (Python)
```python
# requirements.txt - Versiones fijas
tensorflow==2.13.0
flask==2.3.2
flask-socketio==5.3.4
numpy==1.24.3
pandas==2.0.3

# NO agregar dependencias sin aprobación
# NO actualizar versiones sin testing completo
```

### Frontend (TypeScript)
```json
// package.json - Versiones específicas
{
  "dependencies": {
    "react": "^18.2.0",
    "typescript": "^5.0.0",
    "zustand": "^4.3.8"
  }
}

// NO agregar librerías sin justificación
// NO actualizar major versions sin testing
```

## DEBUGGING Y LOGGING

### Logging Estándar
```python
# Backend - Usar logger configurado
from utils.logger import setup_logger
logger = setup_logger()

# Niveles apropiados
logger.debug("Información de debugging")
logger.info("Operación exitosa")
logger.warning("Situación que requiere atención")
logger.error("Error que afecta funcionalidad")
logger.critical("Error crítico del sistema")
```

```typescript
// Frontend - Console logging estructurado
console.group('Training Service');
console.info('Iniciando entrenamiento:', params);
console.warn('Advertencia en configuración:', warning);
console.error('Error en entrenamiento:', error);
console.groupEnd();
```

### Debugging Tools
```bash
# Backend debugging
python -m pdb script.py
python -c "import pdb; pdb.set_trace()"

# Frontend debugging
npm run dev -- --debug
console.log('Debug info:', data);
```

## PERFORMANCE Y MONITOREO

### Métricas Obligatorias
- **Response time**: APIs < 200ms
- **Memory usage**: < 80% del disponible
- **CPU usage**: < 70% en operaciones normales
- **Bundle size**: Frontend < 2MB

### Monitoreo Continuo
```python
# Backend - Monitoreo de recursos
import psutil
import time

def monitor_performance():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    
    if cpu_percent > 80:
        logger.warning(f"CPU usage high: {cpu_percent}%")
    if memory_percent > 85:
        logger.warning(f"Memory usage high: {memory_percent}%")
```

## DOCUMENTACIÓN OBLIGATORIA

### Cuándo Documentar
- **Nuevas APIs**: Siempre documentar endpoints
- **Cambios de interface**: Actualizar documentación existente
- **Arquitectura compleja**: Diagramas y explicaciones
- **Configuración**: Parámetros y opciones

### Formato Estándar
```markdown
# Feature Name

## Descripción
Breve descripción de la funcionalidad.

## API
### Endpoints
- `POST /api/endpoint` - Descripción
- `GET /api/endpoint` - Descripción

### Parámetros
- `param1` (string): Descripción
- `param2` (number): Descripción

## Ejemplos
```python
# Ejemplo de uso
result = api.call_endpoint(param1="value")
```

## Consideraciones
- Limitaciones conocidas
- Dependencias
- Performance implications
```

---

**RECORDATORIO**: Estas reglas garantizan la estabilidad y mantenibilidad del proyecto. Su cumplimiento es OBLIGATORIO para todos los cambios.