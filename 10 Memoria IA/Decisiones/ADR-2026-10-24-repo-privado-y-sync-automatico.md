---
tipo: decision
proyecto: AECODE Nexo Sismico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, git]
---
# Repo privado en GitHub con sincronización por tarea de Windows

## Contexto
El vault es la única fuente de verdad del equipo y la rúbrica exige registro en Git. No había conector de GitHub ni `gh` en la sesión.

## Decisión
Repo privado `FrailM7/nexo-sismico` creado desde el navegador integrado y subido con git (GCM). Sincronización cada 15 min con `09 Cowork/sincronizar.ps1` vía Programador de tareas (`conhost --headless`), que bloquea archivos > 50 MB y patrones de claves/tokens.

## Alternativas descartadas
- **GitHub Desktop manual** — el usuario quería automático.
- **Plugin Obsidian Git** — requiere instalarlo en Obsidian; se dejó como opción para compañeros.

## Consecuencias
- Commits "Sincronizacion automatica …" frecuentes. Conflictos → no sube y queda en el log.
- El log real está en `%LOCALAPPDATA%\NexoSismico\sincronizar.log`; desde la app de Claude (MSIX) se ve una copia virtualizada distinta.

## Relacionado
[[Contexto]] · [[_Indice]]
