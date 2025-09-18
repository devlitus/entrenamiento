# Estándares de Codificación - Neural Network Trainer

## Reglas Generales de Código

### Python (Backend)
- **Estilo**: Seguir PEP 8 estrictamente
- **Límite de líneas**: Máximo 100 líneas por archivo
- **Funciones**: Preferir funciones puras cuando sea posible
- **Imports**: Absolutos desde raíz del proyecto, relativos solo dentro de módulos
- **Variables**: Nombres descriptivos con verbos auxiliares (e.g., isLoading, hasError)
- **Documentación**: Docstrings para todas las funciones públicas

### TypeScript (Frontend)
- **Tipos**: Usar interfaces sobre types, evitar any y enums
- **Componentes**: Funcionales con TypeScript interfaces
- **Exports**: Favorecer named exports sobre default exports
- **Strict Mode**: Habilitado para mejor seguridad de tipos

## Patrones de Arquitectura

### Modularización
- **Separación clara**: Backend Flask + Frontend React independientes
- **Servicios**: Inyección de dependencias, interfaces claras
- **Configuración**: Centralizada en archivos config específicos
- **Logging**: Usar logger configurado, no print() directo

### Estructura de Archivos
- **Componentes**: exported component, subcomponents, helpers, static content, types
- **Directorios**: lowercase con guiones (e.g., components/auth-wizard)
- **Iteración**: Preferir iteración y modularización sobre duplicación

## Herramientas y Librerías

### Backend Stack
- **Framework**: Flask con Flask-SocketIO
- **ML/DL**: TensorFlow/Keras para redes neuronales
- **Datos**: NumPy, Pandas, Scikit-learn
- **Monitoreo**: psutil, GPUtil

### Frontend Stack
- **Framework**: React 19 con TypeScript
- **Estado**: Zustand para gestión de estado
- **Estilos**: TailwindCSS v4 (nunca usar tailwind.config)
- **Comunicación**: Socket.IO + Axios

## Criterios de Calidad

### Mantenibilidad
- Código auto-documentado y legible
- Funciones pequeñas con responsabilidad única
- Evitar anidamiento excesivo
- Manejo adecuado de errores

### Rendimiento
- Optimizar actualizaciones WebSocket
- Evitar re-renders innecesarios en React
- Usar lazy loading cuando sea apropiado
- Cachear datos cuando sea posible

### Seguridad
- Nunca exponer o loggear secretos/keys
- Validar todas las entradas de usuario
- Usar HTTPS en producción
- Sanitizar datos antes de almacenar