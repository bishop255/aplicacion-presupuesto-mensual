@echo off
cd /d "%~dp0"
py presupuesto_app.py
if errorlevel 1 python presupuesto_app.py
if errorlevel 1 pause
