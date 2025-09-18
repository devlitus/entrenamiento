# Workflow de Desarrollo de Funcionalidades

## Proceso de Desarrollo

### 1. Análisis y Planificación
- **Análisis del código base**: Revisar archivos relacionados y dependencias
- **Respuesta en español**: Toda comunicación debe ser en español
- **Plan detallado**: Crear plan específico con pasos numerados
- **No escribir código**: Sin aprobación previa del plan
- **Límite de archivos**: Máximo 100 líneas por archivo

### 2. Diseño de la Funcionalidad
- **Arquitectura modular**: Mantener separación Flask web app + CLI tool
- **Patrones establecidos**: Seguir convenciones existentes del proyecto
- **Reproducibilidad**: Preservar seed=42 y configuraciones
- **Compatibilidad**: Mantener puntos de entrada dual

### 3. Implementación

#### Preparación
- Verificar que no existan conflictos con funcionalidad existente
- Identificar archivos que necesitan modificación
- Planificar estructura de imports y dependencias
- Considerar impacto en testing y documentación

#### Desarrollo
- **Código mínimo**: Solo cambios necesarios para la funcionalidad
- **Archivos relevantes**: Modificar únicamente archivos relacionados
- **Sin cambios adicionales**: Evitar modificaciones no solicitadas
- **Claridad**: Priorizar legibilidad y mantenibilidad

#### Testing
- **pytest**: Cobertura completa de modelos y utilidades
- **Validación**: Verificar integración con sistema existente
- **Regresión**: Asegurar que funcionalidad existente no se rompa
- **Casos edge**: Probar escenarios límite y errores

### 4. Integración

#### Backend
- **Flask**: Seguir patrones de rutas existentes
- **SocketIO**: Mantener formato de eventos de progreso
- **TensorFlow**: Optimización de redes neuronales
- **Streaming**: Server-Sent Events para tiempo real

#### Frontend
- **React 19**: Componentes funcionales con TypeScript
- **Socket.IO**: Comunicación en tiempo real
- **TailwindCSS v4**: Sin usar tailwind.config
- **Estado**: Gestión eficiente con Zustand

### 5. Validación y Documentación

#### Validación
- **Funcionalidad**: Verificar que cumple requisitos
- **Rendimiento**: Comprobar que no degrada performance
- **Compatibilidad**: Asegurar funcionamiento con versiones anteriores
- **Integraciones**: Validar APIs externas (ej: Binance API)

#### Documentación
- **Ubicación**: Documentación en carpeta docs/
- **Formato**: Markdown con estructura clara
- **Ejemplos**: Incluir casos de uso prácticos
- **Actualización**: Mantener documentación sincronizada

## Restricciones Específicas

### Arquitectura
- No modificar estructura del proyecto sin aprobación
- Mantener separación clara CLI/web
- Preservar compatibilidad con run_web.py / run_cli.py
- No agregar dependencias sin justificación explícita

### Código
- Máximo 100 líneas por archivo
- Imports organizados y consistentes
- Logging estructurado (no print directo)
- Manejo de errores robusto

### Machine Learning
- Mantener seeds de reproducibilidad
- Optimizar arquitecturas single/multi-layer
- Normalización consistente de datos
- Métricas de validación apropiadas

## Flujo de Aprobación

### Pre-implementación
1. **Análisis**: Revisar código existente y dependencias
2. **Plan**: Crear plan detallado con pasos específicos
3. **Revisión**: Presentar plan para aprobación
4. **Aprobación**: Esperar confirmación antes de proceder

### Post-implementación
1. **Testing**: Ejecutar suite completa de pruebas
2. **Validación**: Verificar funcionalidad en entorno real
3. **Documentación**: Actualizar documentación relevante
4. **Revisión**: Confirmar que cumple todos los requisitos

## Herramientas y Utilidades

### Desarrollo
- **IDE**: Configuración optimizada para Python/TypeScript
- **Debugging**: Herramientas específicas para ML y web
- **Profiling**: Monitoreo de rendimiento en entrenamientos
- **Version Control**: Git con commits descriptivos

### Testing
- **Unit Tests**: pytest para lógica de negocio
- **Integration Tests**: Pruebas de API y WebSocket
- **E2E Tests**: Validación completa de flujos
- **Performance Tests**: Benchmarks de entrenamiento