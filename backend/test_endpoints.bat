@echo off
REM Script para probar endpoints de la API
REM Asegurate de que el servidor esté corriendo en http://localhost:5000

echo Probando endpoints de la API...
echo.

REM Endpoint básico de estado
echo 1. Probando estado del sistema:
curl -X GET "http://localhost:5000/api/status"
echo.
echo.

REM Información del modelo
echo 2. Probando información del modelo:
curl -X GET "http://localhost:5000/api/model/info"
echo.
echo.

REM Predicción simple
echo 3. Probando predicción simple:
curl -X GET "http://localhost:5000/api/predict?celsius=25"
echo.
echo.

REM Datos de entrenamiento
echo 4. Probando datos de entrenamiento:
curl -X GET "http://localhost:5000/api/training-data"
echo.
echo.

REM Dataset
echo 5. Probando dataset:
curl -X GET "http://localhost:5000/api/dataset"
echo.
echo.

REM Arquitectura actual
echo 6. Probando arquitectura actual:
curl -X GET "http://localhost:5000/api/model/architecture"
echo.
echo.

REM Plantillas disponibles
echo 7. Probando plantillas:
curl -X GET "http://localhost:5000/api/templates"
echo.
echo.

REM Experimentos
echo 8. Probando experimentos:
curl -X GET "http://localhost:5000/api/experiments"
echo.
echo.

REM Estadísticas
echo 9. Probando estadísticas:
curl -X GET "http://localhost:5000/api/statistics"
echo.
echo.

echo Pruebas completadas!
pause