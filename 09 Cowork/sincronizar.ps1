# Sincroniza el vault con GitHub: trae cambios del equipo, revisa que no haya claves y sube lo nuevo.
# Lo ejecuta la tarea programada "Nexo Sismico - sincronizar repositorio" cada 15 minutos.
# Manual:  powershell -ExecutionPolicy Bypass -File "09 Cowork\sincronizar.ps1"
# Registro: %LOCALAPPDATA%\NexoSismico\sincronizar.log (fuera del repositorio)

$repo = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $env:LOCALAPPDATA "NexoSismico"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "sincronizar.log"
$env:GIT_TERMINAL_PROMPT = "0"          # nunca quedarse esperando una contrasena
$env:GCM_INTERACTIVE = "never"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8   # nombres con tildes desde git

function Log($msg) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg" | Out-File -FilePath $log -Append -Encoding utf8 }
function G { $out = & git -C $repo @args 2>&1 | Out-String; $script:code = $LASTEXITCODE; return $out.Trim() }

# Una sola ejecucion a la vez
$mutex = New-Object System.Threading.Mutex($false, "Global\NexoSismicoSync")
if (-not $mutex.WaitOne(0)) { Log "Otra sincronizacion en curso; se omite."; exit 0 }
try {
    # 1. Guardar cambios locales
    G add -A | Out-Null
    $staged = G diff --cached --name-only
    if ($staged) {
        # 1a. Ningun archivo de mas de 50 MB
        $grandes = @()
        foreach ($f in ($staged -split "`r?`n")) {
            $p = Join-Path $repo $f
            if ((Test-Path -LiteralPath $p) -and (Get-Item -LiteralPath $p).Length -gt 50MB) { $grandes += $f }
        }
        # 1b. Ninguna clave o token en las lineas agregadas
        $agregado = (G diff --cached -U0 --no-color) -split "`r?`n" | Where-Object { $_ -match '^\+' -and $_ -notmatch '^\+\+\+' }
        $patrones = '\b\d{8,10}:[A-Za-z0-9_-]{30,}\b', 'sk-[A-Za-z0-9_-]{20,}', 'gh[pousr]_[A-Za-z0-9]{30,}', 'AIza[0-9A-Za-z_-]{30,}',
                    'xox[abp]-[A-Za-z0-9-]{10,}', 'Bearer\s+[A-Za-z0-9._-]{20,}', '(?i)(password|passwd|api[_-]?key|secret)\s*[:=]\s*["'']?[^\s"'']{8,}'
        $sospechoso = $agregado | Where-Object { $l = $_; $patrones | Where-Object { $l -match $_ } }
        if ($grandes -or $sospechoso) {
            G reset -q | Out-Null
            if ($grandes) { Log "DETENIDO: archivos > 50 MB: $($grandes -join ', ')" }
            if ($sospechoso) { Log "DETENIDO: posible clave o token en: $(($sospechoso | Select-Object -First 3) -join ' | ')" }
            exit 2
        }
        $n = ($staged -split "`r?`n").Count
        G commit -q -m "Sincronizacion automatica $(Get-Date -Format 'yyyy-MM-dd HH:mm') ($env:COMPUTERNAME)" | Out-Null
        Log "Commit local con $n archivo(s)."
    }

    # 2. Traer cambios del equipo (rebase sobre origin/main)
    $r = G pull --rebase --autostash -q origin main
    if ($code -ne 0) {
        G rebase --abort | Out-Null
        Log "No se pudieron traer cambios (conflicto o sin red); no se subio nada. Si se repite, resolver con GitHub Desktop. Detalle: $r"
        exit 3
    }

    # 3. Subir
    $ahead = G rev-list --count origin/main..HEAD
    if ([int]$ahead -gt 0) {
        $r = G push -q origin main
        if ($code -ne 0) { Log "ERROR al subir: $r"; exit 4 }
        Log "Subidos $ahead commit(s)."
    }
} finally {
    $mutex.ReleaseMutex() | Out-Null
}
