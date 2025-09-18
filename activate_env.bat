@echo off
call "%~dp0config_paths.bat"
if errorlevel 1 exit /b 1

echo Activando entorno %ENV_NAME%...
call "%CONDA_ACTIVATE%" %ENV_NAME%
echo Entorno %ENV_NAME% activado correctamente!
echo Python version:
python --version
echo.
echo TensorFlow version:
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
cmd /k