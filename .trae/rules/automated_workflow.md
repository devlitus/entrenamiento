# Flujo de Trabajo Automatizado - Neural Network Trainer

## Sistema de Fases Automáticas

### FASE 1: ANÁLISIS AUTOMÁTICO 🔍
```
ANÁLISIS INTELIGENTE DEL PROBLEMA

Ejecuta automáticamente:
- 📁 Examinar estructura de archivos relevantes
- 🔗 Identificar dependencias y conexiones
- 📊 Analizar patrones de código existentes
- 🐛 Localizar causa raíz del problema
- 📋 Generar diagnóstico preliminar

Archivos clave a revisar:
Backend: backend/src/routes.py, backend/src/sockets.py, backend/src/services/
Frontend: frontend/src/components/, frontend/src/services/, frontend/src/store/
Configuración: backend/config.py, frontend/vite.config.ts
```

### FASE 2: PLANIFICACIÓN ESTRATÉGICA 📋
```
DISEÑO DE SOLUCIÓN ÓPTIMA

Ejecuta automáticamente:
- 🎯 Definir objetivos específicos y medibles
- 🔧 Diseñar cambios mínimos necesarios
- 🧪 Planificar tests requeridos
- 📐 Verificar compatibilidad con arquitectura
- ⚡ Estimar impacto en rendimiento

Consideraciones obligatorias:
- ✅ Mantener arquitectura modular Flask + React
- ✅ Preservar comunicación WebSocket existente
- ✅ No modificar seeds de reproducibilidad (seed=42)
- ✅ Seguir patrones de código establecidos
```

### FASE 3: IMPLEMENTACIÓN INTELIGENTE ⚡
```
DESARROLLO AUTOMATIZADO CON VALIDACIÓN

Ejecuta automáticamente:
- 🔨 Aplicar cambios siguiendo code_standards.md
- 🔗 Mantener separación backend/frontend
- 📡 Preservar comunicación tiempo real
- 🧠 Optimizar modelos ML si aplica
- 💾 Actualizar configuraciones necesarias

Patrones obligatorios:
Backend (Python):
- Servicios en backend/src/services/
- Routes en backend/src/routes.py
- SocketIO en backend/src/sockets.py

Frontend (TypeScript):
- Componentes en frontend/src/components/
- Servicios en frontend/src/services/
- Estado en frontend/src/store/
```

### FASE 4: VALIDACIÓN AUTOMÁTICA ✅
```
TESTING Y VERIFICACIÓN COMPLETA

Ejecuta automáticamente:
Backend:
- python -m pytest backend/test_training.py -v
- python backend/verify_architecture.py
- python backend/run_complete_test.py

Frontend:
- cd frontend && npm test
- npm run build
- npm run lint

Validaciones específicas:
- 🔄 Verificar conectividad WebSocket
- 📊 Comprobar Server-Sent Events
- 🧠 Validar modelos ML funcionando
- 📱 Confirmar responsividad UI
```

### FASE 5: PRESENTACIÓN Y DOCUMENTACIÓN 📋
```
RESULTADO FINAL CON EVIDENCIA

Ejecuta automáticamente:
- 👁️ Mostrar preview si hay cambios visuales
- 📊 Generar reporte de cambios realizados
- 🧪 Mostrar resultados de tests
- 📈 Comparar métricas antes/después
- 📝 Documentar cambios en docs/

Entregables:
- ✅ Funcionalidad implementada y validada
- ✅ Tests pasando al 100%
- ✅ Preview visual si aplica
- ✅ Documentación actualizada
```

## Comandos de Activación Rápida

### Para Problemas UI/Frontend:
```
FLUJO-UI: [DESCRIBE PROBLEMA]
```

### Para Issues Backend/API:
```
FLUJO-BACKEND: [DESCRIBE PROBLEMA]
```

### Para Comunicación Tiempo Real:
```
FLUJO-WEBSOCKET: [DESCRIBE PROBLEMA]
```

### Para Optimización ML:
```
FLUJO-ML: [DESCRIBE OBJETIVO]
```

### Para Nuevas Features:
```
FLUJO-FEATURE: [DESCRIBE FUNCIONALIDAD]
```

## Ejemplo de Uso Completo

```
FLUJO-WEBSOCKET: El botón 'Iniciar Entrenamiento' no proporciona feedback visual. Las gráficas no se actualizan en tiempo real y la interfaz se queda en estado fijo.

[El sistema ejecutará automáticamente las 5 fases]
```

## Validaciones Automáticas por Fase

| Fase | Validación Automática | Criterio de Éxito |
|------|----------------------|-------------------|
| 1 | Análisis completo | Causa raíz identificada |
| 2 | Plan viable | Solución compatible con arquitectura |
| 3 | Implementación | Código siguiendo estándares |
| 4 | Tests | 100% tests pasando |
| 5 | Entrega | Preview + documentación |