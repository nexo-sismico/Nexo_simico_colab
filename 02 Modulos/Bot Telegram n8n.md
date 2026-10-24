# Bot de Telegram en n8n (Jean Piere)

Archivos: `05 Datos/Piero JSON/` — revisados el 2026-10-24. **No contienen claves** (las credenciales van en n8n: Telegram Bot RC, OpenAI, Servicio Python RC).

| Flujo | Qué hace |
|---|---|
| RC Bot – Conversación Telegram | Recibe mensajes y botones, maneja sesiones (tablas `rc_bot_sesiones`, `rc_bot_eventos_procesados`), usa un LLM para **extraer parámetros** con esquema estructurado y pide lo que falta; valida con el backend y pide confirmar supuestos |
| RC Bot – Procesar consulta | Crea la consulta en el backend, sondea el estado cada 30 s (máx. 60), avisa si requiere aclaración o si falla |
| RC Bot – Generar y entregar informe | Toma resultados, redacta un artículo con LLM, genera PDF (Gotenberg) y envía PDF y vista 3D por Telegram |

Esquema de extracción del LLM: `estado` ∈ {faltan_datos, requiere_aclaracion, listo_para_validar}, `parametros`, `unidades`, `campos_faltantes`, `inconsistencias`, `supuestos_pendientes`, `siguiente_pregunta`. → **Encaja exacto con las 3 pruebas** (correcto / faltante / equivocado).

## Pendientes para que funcione
- [ ] Backend Python con `GET /schema`, `POST /consultas/validar`, `POST /consultas`, `GET /consultas/{id}` (contrato propuesto, **no implementado**)
- [ ] Reemplazar `BACKEND_URL` y `PDF_SERVICE_URL` (hoy dicen `https://CONFIGURAR-...`)
- [ ] Confirmar el modelo del LLM disponible (los nodos traen nombres por defecto que deben revisarse)
- [ ] El backend debe usar `modelo_final.joblib` del Random Forest
- [ ] Los datos fijados en nodos son ficticios: no usarlos como resultados
