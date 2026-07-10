# Subir el proyecto a GitHub

## Opcion recomendada: GitHub Desktop

1. Abre GitHub Desktop.
2. Elige `File > Add local repository`.
3. Selecciona esta carpeta:

```text
C:\Users\andre\OneDrive\Documentos\Presupuesto_mensual
```

4. Si GitHub Desktop dice que no es repositorio, elige `create a repository`.
5. Revisa que no aparezcan estos archivos para subir:

```text
presupuesto.db
.venv-build/
.venv-exe/
build/
dist/
__pycache__/
tools/
```

6. Haz el primer commit.
7. Usa `Publish repository`.

Antes de publicar, revisa:

```text
docs/CHECKLIST_PUBLICACION.md
```

## Opcion por terminal

Si la carpeta `.git` protegida molesta, elimina esa carpeta manualmente desde el Explorador de Windows y luego ejecuta:

```powershell
git init
git add .
git commit -m "Primera version de Presupuesto Mensual"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/presupuesto-mensual.git
git push -u origin main
```

## Subir el ejecutable

No subas `dist/` al codigo fuente. Para compartir el `.exe`:

1. En GitHub, entra al repositorio.
2. Abre `Releases`.
3. Crea una nueva release, por ejemplo `v1.0.0`.
4. Adjunta:

```text
dist/PresupuestoMensual.exe
```

Asi el repositorio queda limpio y la gente puede descargar la app lista.

## Opcion preparada en esta carpeta

Este proyecto tambien incluye:

```text
subir_github.bat
```

Ese archivo usa el commit preparado localmente y lo sube a:

```text
https://github.com/bishop255/aplicacion-presupuesto-mensual
```

Si Git pide login, completa la ventana de GitHub y vuelve a ejecutar el archivo.
