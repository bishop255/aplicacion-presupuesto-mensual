# Compartir el ejecutable

Para generar el `.exe` en Windows:

1. Instala Python oficial desde `https://www.python.org/downloads/windows/`.
2. Activa `Add python.exe to PATH`.
3. Deja activado `tcl/tk and IDLE`.
4. Ejecuta `build_exe.bat`.

El archivo final queda en:

```text
dist/PresupuestoMensual.exe
```

El icono de la ventana y del `.exe` sale de:

```text
assets/app_icon.ico
```

## Importante

- No subas `presupuesto.db` a GitHub. Ese archivo contiene datos personales.
- Para compartir una version lista para usuarios, sube `PresupuestoMensual.exe` como GitHub Release.
- Si alguien descarga solo el `.exe`, la app creara su propia base local automaticamente.
