---
tags: [cowork, git]
actualizado: 2026-10-24
---
# Sincronización automática con GitHub

Repositorio (privado): **https://github.com/FrailM7/nexo-sismico**

## Qué hace
En el PC de Nicolás, la tarea de Windows **"Nexo Sismico - sincronizar repositorio"** ejecuta `09 Cowork/sincronizar.ps1` cada 15 minutos mientras la sesión está iniciada:
1. Prepara todos los cambios del vault (respetando `.gitignore`: los videos y las credenciales nunca suben).
2. **Se detiene sin subir nada** si encuentra un archivo de más de 50 MB o algo con forma de clave o token (Telegram, OpenAI, GitHub, Google, Slack, `Bearer …`, `password=…`).
3. Hace un commit "Sincronizacion automatica <fecha> (<equipo>)".
4. Trae los cambios del equipo (`pull --rebase`). Si hay conflicto, no sube nada y lo deja anotado.
5. Sube (`push`).

Registro: `%LOCALAPPDATA%\NexoSismico\sincronizar.log` (fuera del repositorio).

## Comandos útiles (PowerShell)
| Para | Comando |
|---|---|
| Sincronizar ya | `Start-ScheduledTask -TaskName "Nexo Sismico - sincronizar repositorio"` |
| Ver el registro | `Get-Content "$env:LOCALAPPDATA\NexoSismico\sincronizar.log" -Tail 20` |
| Pausar | `Disable-ScheduledTask -TaskName "Nexo Sismico - sincronizar repositorio"` |
| Reanudar | `Enable-ScheduledTask -TaskName "Nexo Sismico - sincronizar repositorio"` |
| Quitarla | `Unregister-ScheduledTask -TaskName "Nexo Sismico - sincronizar repositorio" -Confirm:$false` |

## Para los compañeros
- Clonar con GitHub Desktop (File → Clone repository → `nexo-sismico`) y abrir esa carpeta como vault en Obsidian.
- Antes de trabajar: **Fetch/Pull**. Al terminar: **Commit + Push** con un mensaje claro.
- Si alguien quiere lo mismo automático: plugin **Obsidian Git** (auto commit-and-sync cada 10 min) o copiar esta tarea en su PC.

## Si algo sale mal
- "DETENIDO: posible clave o token": revisar el archivo indicado en el registro, quitar la clave y esperar la siguiente ejecución.
- "No se pudieron traer cambios": abrir GitHub Desktop, resolver el conflicto y hacer Push; la tarea sigue sola después.
