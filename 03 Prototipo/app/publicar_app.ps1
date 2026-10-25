# Vuelve a publicar la app web en https://nexo-sismico-nsr10.netlify.app (cuenta Netlify de FrailM7).
# Uso (PowerShell, desde la raíz del repositorio):  powershell -ExecutionPolicy Bypass -File "03 Prototipo\app\publicar_app.ps1"
# La primera vez en un PC: npx netlify-cli login   (abre el navegador para autorizar; requiere acceso al equipo de Netlify)
$ErrorActionPreference = "Stop"
$app = $PSScriptRoot
$sitio = "095e5d3e-1f2b-4a0b-8abf-07b1ccd409c5"      # ID del sitio nexo-sismico-nsr10 (no es secreto)

python (Join-Path $app "construir_sitio.py")
if ($LASTEXITCODE -ne 0) { throw "No se pudo armar el sitio" }
npx --yes netlify-cli@17.38.1 deploy --prod --site $sitio --dir (Join-Path $app "dist") --message "Publicación desde publicar_app.ps1"
