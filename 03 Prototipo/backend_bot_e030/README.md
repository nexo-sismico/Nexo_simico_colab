# Backend para los flujos RC Bot (E.030)

Servicio FastAPI que adapta el artefacto `modelo_final.joblib` del repositorio
ProyectoGH a los endpoints que consumen los tres workflows de n8n.

## Importante: entradas del modelo

Este artefacto necesita **107 características de ingeniería**. No predice de
forma válida a partir de solo pisos, luces y resistencia del concreto. El bot
debe solicitar las características faltantes y no inventarlas. El esquema
`GET /schema` expone nombres, unidades, rangos y ausencia permitida desde los
archivos originales del modelo. Las entradas fuera del dominio de entrenamiento
se rechazan.

El modelo final selecciona configuraciones por respuesta. No se debe describir
como si las ocho salidas fueran exclusivamente Random Forest ni afirmar que son
un análisis estructural o una verificación normativa. Las respuestas son
predicciones dentro del dominio documentado del generador E.030.

## Ejecutar localmente

Requiere Python 3.12 o superior compatible con las versiones fijadas abajo.
Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:BOT_API_TOKEN = 'un-secreto-aleatorio-largo'
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

La raíz queda en `http://127.0.0.1:8000`; la documentación OpenAPI local está
en `/docs`. `GET /health` no requiere autenticación. Todos los endpoints de
consulta e informes exigen `Authorization: Bearer <BOT_API_TOKEN>`.

## Endpoints usados por n8n

- `GET /schema`: entradas, unidades y dominio del modelo.
- `POST /consultas/validar`: campos obligatorios, rangos, valores permitidos y
  coherencia de vanos y unidades declaradas.
- `POST /consultas`: predicción idempotente de ocho respuestas.
- `GET /consultas/{consulta_id}`: resultado para el subflujo del informe.
- `POST /informes/pdf`: recibe `index.html` y `footer.html` como archivos multipart y devuelve el informe PDF.
- `GET /consultas/{consulta_id}/archivos/{archivo_id}`: responde 404; esta
  versión no genera imagen o vista 3D.

La base SQLite local guarda identificadores de consulta y resultados en
`consultas.sqlite3`. Elimina registros vencidos al conectar; por defecto conserva
resultados durante siete días (`BOT_RETENTION_DAYS`). En un despliegue, use
almacenamiento persistente y no publique este archivo. El backend no guarda
`chat_id` ni `user_id`.

## Estado de integración

El contrato coincide con los HTTP nodes de los workflows importados, pero n8n
Cloud no puede acceder a `127.0.0.1`. Para una prueba real de extremo a extremo
falta desplegar este servicio en HTTPS, configurar `BOT_API_TOKEN` en el host,
añadir la misma credencial Bearer a n8n y actualizar `BACKEND_URL` en los tres
workflows. No exponga una instancia local mediante un túnel público sin
autenticación.

Los workflows también necesitan credenciales del proveedor de IA. El endpoint
PDF usa xhtml2pdf, acepta imágenes incrustadas y bloquea la carga de recursos
externos. Esta API todavía no genera archivos 3D. No activar los workflows
hasta conectar el backend, configurar credenciales y completar una prueba real.

## Procedencia del modelo

El archivo del modelo y `modelos_mejorados.py` se copiaron sin reentrenar desde
`PieroVQ/ProyectoGH`, carpeta `resultados_ml_optimizado`, revisada en el vault
el 2026-10-24 (commit `07fd4b2`). `variables_utilizadas.json` y
`diccionario_columnas.json` describen el dominio y las unidades originales.
