# Activa la sincronizacion automatica de este repositorio con GitHub en TU computador (Windows).
# Uso (PowerShell, desde la carpeta del repositorio clonado):
#   powershell -ExecutionPolicy Bypass -File "09 Cowork\instalar_sincronizacion.ps1"
#   powershell -ExecutionPolicy Bypass -File "09 Cowork\instalar_sincronizacion.ps1" -Minutos 10
#   powershell -ExecutionPolicy Bypass -File "09 Cowork\instalar_sincronizacion.ps1" -Quitar
# Requisitos: Git para Windows (winget install Git.Git) y haber clonado el repositorio con tu cuenta de GitHub.
param([int]$Minutos = 15, [switch]$Quitar)

$nombre = "Nexo Sismico - sincronizar repositorio"
if ($Quitar) {
    Unregister-ScheduledTask -TaskName $nombre -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Sincronizacion automatica desactivada." -ForegroundColor Yellow
    exit 0
}

$repo = Split-Path -Parent $PSScriptRoot
$script = Join-Path $PSScriptRoot "sincronizar.ps1"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "No encuentro git. Instala Git para Windows (winget install Git.Git), cierra y abre PowerShell, y vuelve a correr este script." -ForegroundColor Red
    exit 1
}
$origen = git -C $repo remote get-url origin 2>$null
if ($origen -notmatch "nexo-sismico") {
    Write-Host "Esta carpeta no es un clon de nexo-sismico (origin = '$origen'). Clona primero con GitHub Desktop o git clone." -ForegroundColor Red
    exit 1
}
git -C $repo config core.quotepath false
if (-not (git -C $repo config user.name)) {
    $n = Read-Host "Tu nombre para los commits (ej. Alexis Perez)"
    git -C $repo config user.name $n
}
if (-not (git -C $repo config user.email)) {
    Write-Host "Usa tu correo de GitHub o el anonimo: ID+usuario@users.noreply.github.com (GitHub > Settings > Emails)."
    $c = Read-Host "Correo para los commits"
    git -C $repo config user.email $c
}

Write-Host "Probando acceso a GitHub (si se abre el navegador, inicia sesion y autoriza)..."
git -C $repo fetch origin
if ($LASTEXITCODE -ne 0) {
    Write-Host "No pude conectar con GitHub. Revisa que aceptaste la invitacion al repositorio y que iniciaste sesion." -ForegroundColor Red
    exit 1
}

$accion = New-ScheduledTaskAction -Execute "conhost.exe" -Argument "--headless powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$script`""
$disparo = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $Minutos)
$ajustes = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew
$quien = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $nombre -Description "Sincroniza $repo con GitHub cada $Minutos min (09 Cowork\sincronizar.ps1)" -Action $accion -Trigger $disparo -Settings $ajustes -Principal $quien -Force | Out-Null

Write-Host "Primera sincronizacion..."
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Host ""
Write-Host "Listo: este computador sincroniza con GitHub cada $Minutos minutos mientras tengas la sesion iniciada." -ForegroundColor Green
Write-Host "Registro: $env:LOCALAPPDATA\NexoSismico\sincronizar.log"
Write-Host "Para desactivarla: powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Quitar"
