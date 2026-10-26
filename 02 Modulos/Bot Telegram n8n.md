# Bot de Telegram en n8n (Jean Piere)

Archivos: `05 Datos/Piero JSON/` — revisados el 2026-10-24. **No contienen claves** (las credenciales van en n8n: Telegram Bot RC, OpenAI, Servicio Python RC).

| Flujo | Qué hace |
|---|---|
| RC Bot – Conversación Telegram | Recibe mensajes y botones, maneja sesiones (tablas `rc_bot_sesiones`, `rc_bot_eventos_procesados`), usa un LLM para **extraer parámetros** con esquema estructurado y pide lo que falta; valida con el backend y pide confirmar supuestos |
| RC Bot – Procesar consulta | Crea la consulta en el backend, sondea el estado cada 30 s (máx. 60), avisa si requiere aclaración o si falla |
| RC Bot – Generar y entregar informe | Toma resultados, redacta un artículo con LLM, genera PDF (Gotenberg) y envía PDF y vista 3D por Telegram |

Esquema de extracción del LLM: `estado` ∈ {faltan_datos, requiere_aclaracion, listo_para_validar}, `parametros`, `unidades`, `campos_faltantes`, `inconsistencias`, `supuestos_pendientes`, `siguiente_pregunta`. → **Encaja exacto con las 3 pruebas** (correcto / faltante / equivocado).

## Estado de integración en n8n de Joseph (2026-10-25)
- Los tres workflows están importados como borradores y conectados entre sí. Las tablas de sesión y eventos están creadas.
- Credencial de Telegram guardada, probada correctamente y asignada a los once nodos de Telegram. El disparador recibió un mensaje real de prueba.
- La verificación del disparador **no** probó respuestas, IA, cálculo ni PDF; los workflows siguen inactivos.
- Backend inicial en `03 Prototipo/backend_bot_e030/`: carga el artefacto real `modelo_final.joblib`, define el esquema de entradas, valida el dominio y prepara las ocho respuestas que esperan los flujos.
- El modelo requiere **107 entradas** por estructura. No es correcto completar ese esquema inventando datos a partir de una descripción breve.

## Pendientes para completar la integración
- [ ] Instalar dependencias y probar localmente la API contra casos del proyecto; aún no se verificó la carga/ejecución del artefacto desde el servicio nuevo.
- [ ] Elegir alojamiento HTTPS, desplegar el backend con almacenamiento persistente y guardar `BOT_API_TOKEN` como secreto del servicio.
- [ ] Guardar el mismo token como credencial Bearer en n8n y actualizar `BACKEND_URL` en los tres workflows.
- [ ] Crear credenciales del proveedor de IA en n8n y verificar los modelos disponibles. La cuenta actualmente solo muestra Telegram.
- [ ] Configurar la entrega PDF (Gotenberg) o reemplazarla por un generador compatible; no hay servicio PDF configurado.
- [ ] Definir cómo el usuario proporcionará las 107 entradas técnicas (captura conversacional completa o archivo estructurado). El flujo actual recibe texto y botones.
- [ ] Completar archivos 3D del resultado; el backend inicial aún no los genera.
- [ ] Probar el flujo real completo y sus tres casos obligatorios antes de activar workflows.
- [ ] Los datos fijados en nodos son ficticios: no usarlos como resultados.
