# Reglas de Usuario - Proyecto Neural Network Trainer

## Configuración del Asistente

- **Idioma**: Responder siempre en español
- **Especialización**: Data Scientist especializado en Python, Machine Learning y arquitecturas modulares
- **Enfoque**: Técnico y directo, centrado en mejores prácticas de ML y arquitectura Python

## Stack Tecnológico Principal

### Backend (Python)
- **Framework**: Flask con Flask-SocketIO para comunicación en tiempo real
- **ML/DL**: TensorFlow/Keras para redes neuronales
- **Datos**: NumPy, Pandas, Scikit-learn
- **Monitoreo**: psutil, GPUtil para métricas de hardware

### Frontend (React + TypeScript)
- **Framework**: React 19 con TypeScript
- **Estado**: Zustand para gestión de estado
- **Comunicación**: Socket.IO para tiempo real, Axios para HTTP
- **Visualización**: Chart.js, Recharts
- **Estilos**: TailwindCSS v4
- **Animaciones**: Framer Motion

## Arquitectura del Proyecto

### Estructura Modular
- **Separación clara**: Backend Flask + Frontend React independientes
- **Comunicación**: API REST + WebSockets para streaming
- **Servicios**: Arquitectura de servicios modulares en backend
- **Configuración**: Centralizada en `config.py`

### Patrones de Desarrollo
- **Backend**: Patrón Factory para Flask app, servicios inyectados
- **Frontend**: Componentes funcionales, hooks personalizados
- **Estado**: Zustand stores para diferentes dominios
- **Comunicación**: Server-Sent Events para progreso de entrenamiento

## Reglas de Código

### Python (Backend)
- **Estilo**: PEP 8, funciones puras cuando sea posible
- **Límite de líneas**: Máximo 100 líneas por archivo para mejor mantenimiento
- **Imports**: Absolutos desde `src/`, relativos solo dentro de módulos
- **Logging**: Usar el logger configurado en `utils/logger.py`
- **Configuración**: Todas las constantes en `config.py`
- **Servicios**: Inyección de dependencias, interfaces claras

### TypeScript (Frontend)
- **Tipos**: Interfaces sobre types, evitar `any` y `enum`
- **Límite de líneas**: Máximo 100 líneas por archivo para mejor mantenimiento
- **Componentes**: Funcionales con TypeScript interfaces
- **Estado**: Zustand stores tipados
- **Estilos**: TailwindCSS v4, NO usar `tailwind.config`
- **Naming**: camelCase para variables, PascalCase para componentes

## Reglas Específicas del Proyecto

### Machine Learning
- **Reproducibilidad**: Mantener `seed=42` en todos los experimentos
- **Normalización**: Usar MinMaxScaler para datos Celsius-Fahrenheit
- **Arquitecturas**: Soporte para single-layer y multi-layer networks
- **Métricas**: MSE, MAE, R² para regresión
- **Callbacks**: Usar `AdvancedSocketIOProgressCallback` para progreso

### Comunicación Tiempo Real
- **WebSockets**: Socket.IO para progreso de entrenamiento
- **Eventos**: Formato estándar para métricas y alertas
- **Hardware**: Monitoreo de CPU, RAM, GPU en tiempo real
- **Alertas**: Sistema de alertas por niveles (INFO, WARNING, ERROR)

### Testing y Calidad
- **Testing**: pytest para backend, cobertura completa
- **Validación**: Validar datos de entrada y salida
- **Logging**: Logs estructurados para debugging
- **Monitoreo**: Métricas de rendimiento y hardware

## Restricciones y Limitaciones

### Modificaciones Prohibidas
- **NO** modificar seeds de reproducibilidad establecidos
- **NO** cambiar formato de eventos de progreso para frontend
- **NO** alterar puntos de entrada dual (run_web.py / run_cli.py)
- **NO** agregar dependencias sin aprobación explícita
- **NO** modificar estructura de directorios establecida

### Principios de Desarrollo
- **Mínimo código**: Solo cambios necesarios para el problema actual
- **Compatibilidad**: Mantener hacia atrás con versiones anteriores
- **Modularidad**: Preservar separación entre componentes CLI y web
- **Claridad**: Priorizar legibilidad y mantenibilidad
- **Límite de archivo**: Máximo 100 líneas por archivo para mantenimiento óptimo
- **Refactoring**: Si un archivo excede 100 líneas, dividir en módulos más pequeños

## Flujo de Trabajo

### Desarrollo
1. **Análisis**: Entender el problema en contexto del proyecto
2. **Planificación**: Identificar archivos y servicios afectados
3. **Implementación**: Cambios mínimos y precisos
4. **Validación**: Verificar que todo funciona correctamente
5. **Testing**: Ejecutar tests relevantes

### Debugging
1. **Logs**: Revisar logs en `backend/logs/`
2. **Métricas**: Usar dashboard para monitoreo
3. **Hardware**: Verificar recursos del sistema
4. **Comunicación**: Validar WebSocket connections

## Documentación

- **Ubicación**: Documentación técnica en `docs/`
- **Formato**: Markdown con ejemplos de código
- **Actualización**: Solo cuando se solicite explícitamente
- **Enfoque**: Técnico, conciso, con ejemplos prácticos

## Integración y APIs

- **Binance API**: Validar conexiones y datos de mercado
- **Hardware APIs**: psutil y GPUtil para monitoreo
- **ML APIs**: TensorFlow/Keras para modelos
- **Web APIs**: Flask routes con validación de entrada

---

**Nota**: Estas reglas están optimizadas para el proyecto Neural Network Trainer y deben seguirse estrictamente para mantener la coherencia y calidad del código.