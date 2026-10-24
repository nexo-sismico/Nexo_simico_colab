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
| `ficha.py` | Ficha de pruebas de 1 página (PDF) |
| `informe.js` | Informe tipo artículo (DOCX; convertir a PDF con Word o LibreOffice) |
| `deck.js` | Presentación (PPTX) con notas del orador |
| `videos.py` | Videos del prototipo y ejecutivo (MP4 con subtítulos) y sus .srt |
| `casos/*.json` | Caso 1 completo (grupo 1, Piedemonte A), caso 2 sin Fv, caso 3 con altura en cm |
| `desplazamientos_excel.json` | Desplazamientos de las 12 combinaciones (hojas Der-E5 y Der-A1 del Excel del curso) |

## Orden de ejecución
```
python correr_pruebas.py        # prototipo: 3 casos
python base_datos_nsr10.py      # base NSR-10 (19 registros)
python experimento_ml.py        # métricas Random Forest
python numeros.py               # cifras para informe y PPT
python figuras.py
python ficha.py
node informe.js                 # requiere: npm install docx
node deck.js                    # requiere: npm install pptxgenjs react react-dom react-icons sharp
python videos.py                # requiere ffmpeg, python-pptx, Pillow y el PDF de la presentación
```
Requisitos Python: 3.10+, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `openpyxl`, `reportlab`.
`deck.js` usa además un script de tema (`apply_theme.js`) del entorno donde se generó; si no está, comentar esas dos líneas y el deck sale con los colores por defecto.

Para un edificio nuevo: copiar `casos/caso1_completo.json`, cambiar los valores y llamar `analizar()` de `nexo_nsr10.py`.
Sin claves ni tokens en ningún archivo.
