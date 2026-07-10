# Contribuir

Gracias por revisar este proyecto.

## Como trabajar el codigo

1. Crea o activa un entorno de Python.
2. Ejecuta la app con:

```powershell
python presupuesto_app.py
```

3. Mantén la separacion de responsabilidades:

- Interfaz: `presupuesto/app.py`
- Datos y calculos: `presupuesto/store.py`
- Utilidades: `presupuesto/utils.py`
- Ventanas emergentes: `presupuesto/dialogs.py`
- Constantes: `presupuesto/constants.py`

## Antes de subir cambios

Ejecuta:

```powershell
python -m py_compile presupuesto_app.py presupuesto/app.py presupuesto/store.py presupuesto/utils.py presupuesto/dialogs.py presupuesto/constants.py
```

No subas `presupuesto.db`, carpetas `.venv-*`, `build/` ni `dist/`.

