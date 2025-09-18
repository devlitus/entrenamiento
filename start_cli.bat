@echo off
call "%~dp0config_paths.bat"
if errorlevel 1 exit /b 1

echo Activando entorno %ENV_NAME%...
call "%CONDA_ACTIVATE%" %ENV_NAME%
echo Entorno activado. Puedes usar los comandos CLI ahora.
echo Ejemplo: python backend/run_cli.py --help
cmd /k