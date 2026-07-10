@echo off
cd /d "%~dp0"
setlocal

set "PYTHON_CMD="
set "BUILD_PYTHON=.venv-exe\Scripts\python.exe"

if exist "%BUILD_PYTHON%" goto validate_build_python

where py >nul 2>nul
if %errorlevel%==0 set "PYTHON_CMD=py -3"

if "%PYTHON_CMD%"=="" (
    where python >nul 2>nul
    if %errorlevel%==0 set "PYTHON_CMD=python"
)

if "%PYTHON_CMD%"=="" (
    echo No encontre Python instalado en Windows.
    echo Instala Python desde https://www.python.org/downloads/windows/
    echo Marca la opcion "Add python.exe to PATH" durante la instalacion.
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import tkinter, _tkinter; print('Tkinter OK')" >nul 2>nul
if errorlevel 1 (
    echo Python existe, pero no tiene Tkinter funcionando.
    echo Instala Python oficial desde https://www.python.org/downloads/windows/
    echo En el instalador deja activada la opcion "tcl/tk and IDLE".
    pause
    exit /b 1
)

if not exist ".venv-exe\Scripts\python.exe" (
    %PYTHON_CMD% -m venv .venv-exe
)

:validate_build_python
"%BUILD_PYTHON%" -c "import tkinter, _tkinter; print('Tkinter OK')" >nul 2>nul
if errorlevel 1 (
    echo El entorno .venv-exe existe, pero no tiene Tkinter funcionando.
    echo Borra la carpeta .venv-exe y vuelve a ejecutar este archivo con Python oficial instalado.
    pause
    exit /b 1
)

"%BUILD_PYTHON%" -m pip install --upgrade pip pillow pyinstaller
"%BUILD_PYTHON%" scripts\generate_icon.py
"%BUILD_PYTHON%" -m PyInstaller --clean --onefile --windowed --name PresupuestoMensual --icon assets\app_icon.ico --add-data "assets\app_icon.ico;assets" presupuesto_app.py

echo.
echo Ejecutable generado en:
echo %cd%\dist\PresupuestoMensual.exe
pause
