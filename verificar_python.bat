@echo off
cd /d "%~dp0"
echo Revisando Python para crear el ejecutable...
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 -c "import sys, tkinter; root=tkinter.Tk(); root.destroy(); print('Python OK:', sys.executable); print('Tkinter OK')"
    if not errorlevel 1 goto ok
)

where python >nul 2>nul
if %errorlevel%==0 (
    python -c "import sys, tkinter; root=tkinter.Tk(); root.destroy(); print('Python OK:', sys.executable); print('Tkinter OK')"
    if not errorlevel 1 goto ok
)

echo No encontre un Python oficial funcionando con Tkinter.
echo.
echo Solucion:
echo 1. Instala Python desde https://www.python.org/downloads/windows/
echo 2. Marca "Add python.exe to PATH".
echo 3. En opciones, deja activado "tcl/tk and IDLE".
echo 4. Cierra y vuelve a abrir Codex o reinicia Windows.
echo.
pause
exit /b 1

:ok
echo.
echo Todo listo. Ahora puedes ejecutar build_exe.bat.
pause
