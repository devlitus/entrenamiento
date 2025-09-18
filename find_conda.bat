@echo off
echo Buscando instalación de Conda...
echo.

REM Ubicaciones comunes de Conda
set LOCATIONS[0]=C:\Users\%USERNAME%\miniconda3
set LOCATIONS[1]=C:\Users\%USERNAME%\anaconda3
set LOCATIONS[2]=C:\ProgramData\Miniconda3
set LOCATIONS[3]=C:\ProgramData\Anaconda3
set LOCATIONS[4]=C:\tools\miniconda3
set LOCATIONS[5]=C:\tools\anaconda3
set LOCATIONS[6]=C:\miniconda3
set LOCATIONS[7]=C:\anaconda3

echo Verificando ubicaciones comunes:
echo.

for /L %%i in (0,1,7) do (
    call set "CURRENT_PATH=%%LOCATIONS[%%i]%%"
    call :check_path "!CURRENT_PATH!"
)

echo.
echo Si no se encontró tu instalación, verifica manualmente:
echo 1. Abre Anaconda Prompt
echo 2. Ejecuta: conda info --base
echo 3. Usa esa ruta en config_paths.bat
echo.
pause
goto :eof

:check_path
set "TEST_PATH=%~1"
if exist "%TEST_PATH%\Scripts\activate.bat" (
    echo ✓ ENCONTRADO: %TEST_PATH%
    echo   Para usar esta ubicación, edita config_paths.bat:
    echo   set CONDA_PATH=%TEST_PATH%
    echo.
) else (
    echo ✗ No encontrado: %TEST_PATH%
)
goto :eof