# Checklist de publicacion

Antes de subir a GitHub, confirma:

- [ ] `presupuesto.db` no se sube.
- [ ] `.venv-build/` y `.venv-exe/` no se suben.
- [ ] `build/` y `dist/` no se suben como codigo fuente.
- [ ] `__pycache__/` no se sube.
- [ ] `README.md` se ve bien en GitHub.
- [ ] El ejecutable se comparte como `Release`, no como archivo del repositorio.

## Archivos principales que si deben quedar en GitHub

```text
.github/
assets/
docs/
presupuesto/
scripts/
.gitattributes
.gitignore
abrir_presupuesto.bat
build_exe.bat
CHANGELOG.md
COMPARTIR.md
CONTRIBUTING.md
LICENSE
presupuesto_app.py
pyproject.toml
README.md
requirements-build.txt
requirements.txt
verificar_python.bat
```

