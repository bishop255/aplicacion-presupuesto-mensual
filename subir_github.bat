@echo off
cd /d "%~dp0"
setlocal

echo Subiendo Presupuesto Mensual a GitHub...
echo.

git --git-dir=.git-publish --work-tree=. remote set-url origin https://github.com/bishop255/aplicacion-presupuesto-mensual.git
git --git-dir=.git-publish --work-tree=. branch -M main
git --git-dir=.git-publish --work-tree=. push -u origin main

if errorlevel 1 (
    echo.
    echo No se pudo subir automaticamente.
    echo Si aparece una ventana de GitHub, inicia sesion y vuelve a ejecutar este archivo.
    echo Tambien puedes publicar con GitHub Desktop usando esta carpeta.
    pause
    exit /b 1
)

echo.
echo Listo. Proyecto publicado en:
echo https://github.com/bishop255/aplicacion-presupuesto-mensual
pause
