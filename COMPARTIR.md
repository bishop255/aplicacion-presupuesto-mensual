# Como compartir la app

Tienes dos caminos simples:

## Opcion rapida

Comparte esta carpeta completa:

`C:\Users\andre\OneDrive\Documentos\Presupuesto_mensual`

Tu amigo debe abrir `abrir_presupuesto.bat`. Necesita tener Python instalado en Windows.

Si quieres compartir la app sin tus datos personales, no incluyas `presupuesto.db`. Al abrirla, la app creara una base nueva con los gastos base.

## Opcion mas comoda para otra persona

Lo ideal es convertirla en un archivo `.exe`, asi tu amigo no necesita instalar Python. Para generar el ejecutable:

1. Instala Python oficial desde `https://www.python.org/downloads/windows/`.
2. En el instalador marca `Add python.exe to PATH`.
3. Deja activada la opcion `tcl/tk and IDLE`.
4. Ejecuta `build_exe.bat`.

El ejecutable quedara en la carpeta `dist`.

Si quieres compartir la app sin tus datos personales, envia solo `dist\PresupuestoMensual.exe` y no envies `presupuesto.db`.
