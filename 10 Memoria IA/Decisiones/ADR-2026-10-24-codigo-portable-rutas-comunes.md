---
tipo: decision
proyecto: AECODE Nexo Sismico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, codigo]
---
# Código del prototipo portable con `rutas.py`

## Contexto
Los scripts se escribieron en Linux: rutas relativas a `resultados/` (que vive en `07 Outputs/Prototipo NSR-10`), fuentes en `/usr/share/fonts`, `open()` sin UTF-8 (en Windows salía "mÃ¡x"), `apply_theme.js` en `/mnt/skills`.

## Decisión
`rutas.py` centraliza rutas (COD, SAL, RES, FIG, ENT) y busca fuentes (Liberation→Arial→DejaVu de matplotlib); stdout UTF-8. `ejecutar_todo.py` corre la cadena; `requirements.txt` y `package.json`. JS usa `__dirname`; `apply_theme` opcional.

## Alternativas descartadas
- **`os.chdir` a 07 Outputs en cada script** — menos explícito para el equipo.
- **Commitear los resultados regenerados** — difieren en el 4.º decimal (paralelismo sklearn) y los figuras/PPT sin tema; se restauraron los versionados.

## Consecuencias
- Cadena verificada en Windows (Python 3.13). `videos.py` requiere ffmpeg (no instalado, no probado).

## Relacionado
[[Contexto]] · [[_Indice]]
