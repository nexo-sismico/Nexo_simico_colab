---
tipo: decision
proyecto: Nexo Sísmico
fecha: 2026-10-24
estado: aceptada
reemplaza:
tags: [decision, frontend, prototipo]
---
# Interfaz del prototipo: app web que ejecuta nexo_nsr10.py en el navegador (Pyodide)

## Contexto
El prototipo funcionaba en consola. Para que lo usen ingenieros hacía falta una interfaz interactiva, sin perder la trazabilidad del cálculo ya validado contra Excel + SAP2000.

## Decisión
App web estática en `03 Prototipo/app/` (HTML + CSS + JS, Chart.js) que carga el mismo `03 Prototipo/codigo/nexo_nsr10.py` con Pyodide y lo ejecuta en el navegador. Se abre con `python "03 Prototipo/app/abrir_app.py"`.

## Alternativas descartadas
- **Reescribir el cálculo en JavaScript** — dos implementaciones que pueden divergir; se pierde la validación hecha.
- **Servidor Python (Flask/FastAPI)** — obliga a instalar dependencias y mantener un servidor; la app estática corre igual en cualquier PC y se puede hospedar gratis.
- **Streamlit** — rápido, pero menos control de la interfaz y requiere servidor.
- **Publicarla como Artifact de Claude** — su política de contenido bloquea las descargas de Pyodide.

## Consecuencias
- La primera carga necesita internet (Pyodide ≈ 10 MB, luego queda en caché).
- Cualquier cambio en `nexo_nsr10.py` se refleja en la app sin tocarla.
- Publicada en Netlify: https://nexo-sismico-nsr10.netlify.app. Solo se sube la carpeta `dist` que arma `construir_sitio.py`; la protección de equipo que Netlify activa por defecto se desactivó solo en este sitio.
- Pendiente: conectar el bot de Telegram al mismo motor.

## Relacionado
[[Contexto]] · [[_Indice]] · [[ADR-2026-10-24-codigo-portable-rutas-comunes]]
