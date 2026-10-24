---
tags: [coordinacion, ruta]
actualizado: 2026-10-24
---
# Ruta de trabajo y coordinación

> Una sola fuente de verdad: este vault (repositorio Git del grupo). Lo que no esté aquí, no existe para la entrega.

## 1. Qué hay que entregar
| # | Entregable | Formato | Límite | Responsable final | Fecha |
|---|---|---|---|---|---|
| E1 | Prototipo funcionando probado con 3 casos (correcto, falta un dato, dato equivocado) | Bot o notebook | — | Joseph (integra) + técnicos | **Hoy** |
| E2 | Video del prototipo | MP4 | **≤ 2 min** | Joseph | **Hoy** |
| E3 | Ficha de pruebas | PDF 1 página, enlace o capturas, **sin claves** | 1 pág. | Nicolás + Joseph | **Hoy** |
| E4 | Video ejecutivo | MP4 | ≤ 5 min | Joseph | Demo Day |
| E5 | Presentación | PPT | — | Todos, integra Joseph | Demo Day |
| E6 | Informe tipo artículo | PDF | ≤ 5 págs. | Lucero revisa, Joseph integra | Demo Day |
| E7 | Registro en Git | `REGISTRO_EQUIPO.md` | — | Nicolás | Hoy |
| E8 | Evidencia en Miro y Discord | Tablero + canal | — | Joseph | Continuo |

## 2. Decisión del prototipo de hoy — ✅ TOMADA: ruta B (módulo NSR-10)

El prototipo B está listo y probado (ver [[Pruebas 3 casos]]). El informe presenta **ambas** líneas según [[Flujo integrado de herramientas]]. Contexto de la decisión:
El bot de Piero (n8n) depende de un **servicio Python que aún no existe** (`/schema`, `/consultas/validar`, `/consultas`). Opciones:

| Opción | Qué se muestra | Riesgo | Recomendación |
|---|---|---|---|
| **A. Bot n8n + validador mínimo** | Conversación en Telegram que detecta faltantes y errores (los 3 casos encajan con `faltan_datos` / `inconsistencias`) | Hay que levantar un backend mínimo y credenciales | **Prototipo del equipo** si alguien tiene n8n operativo |
| **B. Módulo NSR-10 con validación** | Notebook que valida entradas y calcula sismo, pesos, FHE, derivas para el edificio del grupo 1 | Bajo: ya corre | **Respaldo seguro** y parte de Nicolás |
| C. Random Forest en Colab | Predicción de derivas con 3 entradas | Requiere `modelo_final.joblib` de Jean Piere | Complemento |

Regla: el video de hoy muestra **una** ruta completa (A o B). Lo demás se menciona como siguiente paso.

## 3. Quién hace qué hoy
| Persona | Tarea de hoy | Entrega en el vault |
|---|---|---|
| **Nicolás** | ✅ Prototipo B con 3 casos y ficha · ✅ base NSR-10 (19 registros) · publicar repositorio Git · texto del módulo para el informe | `03 Prototipo/`, `07 Outputs/`, `REGISTRO_EQUIPO.md` |
| **Jean Piere** | Confirmar si el bot n8n corre; si sí, backend mínimo o datos fijados para los 3 casos; compartir `modelo_final.joblib` y métricas | `02 Modulos/Bot Telegram n8n.md`, `05 Datos/` |
| **Alexis** | Una familia OpenSees documentada (tabla + imagen 3D) para el video y el informe | `02 Modulos/Generador OpenSees E030.md` |
| **Lucero** | Introducción, pregunta, objetivos, ejes y referencias para informe y PPT | `04 Entregables/Informe tipo articulo.md` |
| **Joseph** | Grabar video ≤ 2 min, integrar ficha, subir entregables, actualizar Miro | `04 Entregables/`, `08 Multimedia/` (enlace) |

## 4. Secuencia (orden de dependencias)
1. Decidir A o B (15 min, Discord).
2. Correr los 3 casos y guardar capturas en `07 Outputs/Prototipo/`.
3. Llenar [[Pruebas 3 casos]] con resultados reales.
4. Armar [[Ficha 1 pagina]] → PDF.
5. Grabar con [[Guion video 2 min]] (revisar que no salgan claves, tokens ni chat IDs).
6. Commit + Push en GitHub y subir entregables a la plataforma.

## 5. Checklist de cierre (marcar antes de enviar)
- [x] Los 3 casos están probados y con captura
- [x] El video dura ≤ 2 min y muestra el prototipo funcionando (1:58)
- [x] La ficha es de 1 página y tiene enlace o capturas
- [ ] Ninguna clave, token, chat ID ni URL privada aparece en video, capturas o repositorio
- [ ] `REGISTRO_EQUIPO.md` completo (faltan habilidades de 4 integrantes)
- [ ] Datos provisionales marcados como tales (V7 de ejemplo, datos ficticios del bot)

## 6. Mensaje para el grupo (copiar en Discord)
> Equipo: ya está el vault/repositorio con todo ordenado. La ruta de hoy está en `01 Proyecto/Ruta de trabajo y coordinacion.md`. Necesitamos decidir en 15 min si el prototipo de hoy es el bot de Telegram (Piero, ¿n8n está corriendo?) o el módulo NSR-10 (respaldo que ya funciona). Cada uno revise su fila en "Quién hace qué hoy" y suba su parte al repositorio.

## 7. Estado al cierre del 24 oct (Nicolás)
Todos los entregables tienen versión 1 en `04 Entregables/`: informe (4 págs.), presentación (14 diap.), ficha, guiones y videos (en `08 Multimedia`, por enlace).
Pendiente del equipo: (1) cada uno completa su fila de habilidades en `REGISTRO_EQUIPO.md`; (2) Jean Piere agrega métricas E.030 si las tiene; (3) Joseph sube los videos a Drive/YouTube y pega los enlaces; (4) grabar voz sobre el video ejecutivo si se quiere narración; (5) Miro y Discord con las decisiones de [[Decisiones]].
