@echo off
REM ============================================
REM CONFIGURACIÓN DE RUTAS - Neural Trainer
REM ============================================
REM 
REM Si cambias la ubicación de Miniconda3, 
REM solo modifica esta línea:
REM
set CONDA_PATH=C:\Users\carle\miniconda3
REM
REM ============================================

REM No modificar estas líneas
set CONDA_ACTIVATE=%CONDA_PATH%\Scripts\activate.bat
set ENV_NAME=neural-trainer

REM Verificar si existe la ruta
if not exist "%CONDA_ACTIVATE%" (
    echo ERROR: No se encontró Conda en: %CONDA_PATH%
    echo.
    echo Posibles ubicaciones comunes:
    echo - C:\Users\%USERNAME%\miniconda3
    echo - C:\Users\%USERNAME%\anaconda3
    echo - C:\ProgramData\Miniconda3
    echo - C:\tools\miniconda3
    echo.
    echo Por favor, actualiza CONDA_PATH en config_paths.bat
    pause
    exit /b 1
)

echo Configuración cargada correctamente:
echo - Conda Path: %CONDA_PATH%
echo - Environment: %ENV_NAME%