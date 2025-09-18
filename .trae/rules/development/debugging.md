# Guía de Debugging - Neural Network Trainer

## Proceso de Debugging Paso a Paso

### 1. Reproducir el Error
- Ejecutar el programa en las condiciones que provocan el fallo
- Asegurar que el error sea consistente y repetible
- Documentar los pasos exactos para reproducir el problema

### 2. Analizar el Mensaje de Error
- Leer y comprender el mensaje de error completo
- Identificar el tipo de error: sintaxis, lógico, runtime, etc.
- Observar la línea donde ocurre y el tipo de excepción

### 3. Revisar el Código Afectado
- Localizar la sección del código donde ocurre el problema
- Comprender la lógica que debería ejecutarse
- Comparar con lo que realmente hace el código

### 4. Usar Herramientas de Debug

#### Breakpoints
- Establecer puntos de interrupción en el IDE
- Detener la ejecución en puntos clave
- Inspeccionar el estado del programa en tiempo real

#### Inspección de Variables
- Observar los valores de las variables en cada paso
- Verificar si contienen valores esperados
- Identificar valores nulos, inesperados o mal calculados

#### Trazas y Logs
- Usar el logger configurado del proyecto (no print directo)
- Añadir mensajes para seguir el flujo de ejecución
- Útil para entender qué partes del código se ejecutan y en qué orden

### 5. Aislar el Problema
- Reducir el código a la mínima expresión que reproduzca el error
- Crear casos de prueba específicos
- Facilitar la identificación de la causa raíz

### 6. Corregir y Verificar
- Modificar el código para solucionar el problema
- Asegurar que el cambio no afecte otras partes del programa
- Ejecutar pruebas para confirmar la resolución
- Realizar pruebas adicionales para evitar regresiones

## Herramientas Específicas del Proyecto

### Backend (Python)
- **Logger**: Usar `utils.logger` configurado
- **Testing**: pytest para pruebas automatizadas
- **Profiling**: Para problemas de rendimiento en ML
- **TensorFlow Debug**: Para problemas en redes neuronales

### Frontend (React)
- **React DevTools**: Para debugging de componentes
- **Browser DevTools**: Para debugging de JavaScript
- **Network Tab**: Para problemas de comunicación con backend
- **Socket.IO Debug**: Para problemas de WebSocket

### Integración
- **WebSocket**: Verificar conexión y eventos en tiempo real
- **API**: Usar herramientas como Postman para probar endpoints
- **Database**: Verificar integridad de datos en SQLite
- **Hardware Monitor**: Revisar métricas de sistema durante entrenamiento

## Errores Comunes del Proyecto

### Machine Learning
- **Overfitting/Underfitting**: Revisar métricas de validación
- **NaN en pérdidas**: Verificar learning rate y normalización
- **Memoria insuficiente**: Monitorear uso de GPU/CPU
- **Convergencia lenta**: Ajustar hiperparámetros

### Comunicación Frontend-Backend
- **CORS**: Verificar configuración de orígenes permitidos
- **WebSocket**: Confirmar eventos y callbacks
- **Serialización**: Verificar formato JSON de datos
- **Timeouts**: Ajustar tiempos de espera para entrenamientos largos