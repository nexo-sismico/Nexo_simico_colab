# Código — Módulo NSR-10, base de datos, aprendizaje y entregables

| Archivo | Qué hace |
|---|---|
| `nexo_nsr10.py` | Valida la entrada y calcula NSR-10: espectro, Cu·Ta, FHE, torsión accidental, derivas (12 combinaciones, 2 esquinas), Q y R |
| `correr_pruebas.py` | Corre los 3 casos de prueba y guarda reportes en `resultados/` |
| `base_datos_nsr10.py` | Une los 18 edificios teóricos del profesor y los casos del módulo en `base_datos_NSR10.csv` |
| `config_plantas_profesor.py` | Entradas (luces, pisos, uso, cargas) de los 20 edificios enviados al profesor |
| `Resumen_resultados_profesor.xlsx` | Resultados del profesor (18 edificios; P9 falló en su dimensionamiento) |
| `experimento_ml.py` | Random Forest vs regresión lineal vs referencias, validación dejando una planta fuera |
| `numeros.py` | Junta en `numeros.json` las cifras que usan el informe y la presentación |
| `figuras.py` | Figuras del informe y la presentación (`figuras/`) |
| `ficha.py` | Ficha de pruebas de 1 página (PDF), copia en `04 Entregables/Prototipo` |
| `rutas.py` | Rutas comunes (codigo, 07 Outputs, 04 Entregables) y búsqueda de fuentes en cualquier sistema |
| `ejecutar_todo.py` | Corre toda la cadena en orden |
| `equipo.json` | **Nombres oficiales** de los integrantes (los leen informe, presentación, ficha y demo) |
| `demo_en_vivo.py` | Demostración en vivo de las 3 pruebas para grabar el video del Reto 06 (≈ 1:20; `--rapido` para revisar) |
| `prototipo_docs.py` | Esquema del prototipo y `Definicion_prototipo.pdf` (problema, flujo, límites, pruebas, medición) |
| `resumen_e030.py` | Resultados de la ruta E.030 (repositorio de Jean Piere): entrena Random Forest con su partición y escribe `07 Outputs/E030/` para el informe y la PPT. Uso: `python resumen_e030.py RUTA/ProyectoGH` |
| `informe.js` | Informe tipo artículo (DOCX; convertir a PDF con Word o LibreOffice) |
| `deck.js` | Presentación (PPTX) con notas del orador |
| `videos.py` | Videos del prototipo y ejecutivo (MP4 con subtítulos) y sus .srt |
| `casos/*.json` | Caso 1 completo (grupo 1, Piedemonte A), caso 2 sin Fv, caso 3 con altura en cm |
| `desplazamientos_excel.json` | Desplazamientos de las 12 combinaciones (hojas Der-E5 y Der-A1 del Excel del curso) |

## Cómo ejecutarlo (Windows, macOS, Linux o Colab)
Los scripts ya no dependen de la carpeta desde donde se llamen ni de fuentes de Linux (`rutas.py` resuelve rutas y fuentes).
Las salidas van a `07 Outputs/Prototipo NSR-10/` y los entregables a `04 Entregables/`.

```
pip install -r "03 Prototipo/codigo/requirements.txt"
python "03 Prototipo/codigo/ejecutar_todo.py"             # pruebas → base (19) → ML → cifras → figuras → ficha
python "03 Prototipo/codigo/ejecutar_todo.py" --informe   # + informe DOCX y presentación PPTX (antes: npm install en esta carpeta)
python "03 Prototipo/codigo/ejecutar_todo.py" --videos    # + videos (requiere ffmpeg: winget install Gyan.FFmpeg)
```
También se puede correr cada script por separado, en el mismo orden: `correr_pruebas.py`, `base_datos_nsr10.py`, `experimento_ml.py`, `numeros.py`, `figuras.py`, `ficha.py`.

Notas:
- Las métricas del Random Forest pueden variar en el 4.º decimal entre equipos (paralelismo de scikit-learn); las cifras del informe (3 decimales) no cambian.
- `deck.js` usa `apply_theme.js` solo si existe (variable `APPLY_THEME`); sin él, el PPTX sale con colores por defecto. Por eso el PPTX versionado no se regenera salvo que se cambie su contenido.
- El PDF del informe se obtiene abriendo el DOCX en Word → Guardar como PDF.

Para un edificio nuevo: copiar `casos/caso1_completo.json`, cambiar los valores y llamar `analizar()` de `nexo_nsr10.py`.
Sin claves ni tokens en ningún archivo.
