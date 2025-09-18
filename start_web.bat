@echo off
call "%~dp0config_paths.bat"
if errorlevel 1 exit /b 1

echo Activando entorno %ENV_NAME%...
call "%CONDA_ACTIVATE%" %ENV_NAME%
echo Iniciando servidor web...
cd backend
python server.py
pause