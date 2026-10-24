# App web · Nexo Sísmico NSR-10

Interfaz para ingenieros del prototipo: verificación sísmica preliminar NSR-10 de edificios aporticados de concreto, en el navegador.

![App web del verificador NSR-10](../../04%20Entregables/Prototipo/capturas/app_web_verificar.png)

## Abrirla
```bash
python "03 Prototipo/app/abrir_app.py"
```
Abre `http://127.0.0.1:8765/03 Prototipo/app/index.html` en el navegador. Solo necesita Python (biblioteca estándar) e internet la primera vez, para descargar Pyodide y Chart.js.

## Qué hace
| Paso | En la app |
|---|---|
| 1. Datos | Formulario por bloques: proyecto, sitio (Aa, Av, Fa, Fv, TL, grupo de uso), sistema (R0, φa, φr), geometría y pesos por nivel, periodos de SAP2000 |
| 2. Desplazamientos | **Pegar tabla de SAP2000** (`Joint Displacements`: Joint, OutputCase, U1, U2) e indicar el nudo de cada nivel en dos esquinas opuestas; también acepta el formato `Esquina, Combinacion, Nivel, U1, U2` |
| 3. Revisión en vivo | Mientras escribe, marca en amarillo lo que falta y en rojo lo que está fuera de rango, con enlace a cada campo |
| 4. Verificar | Si algo falta o está mal, se detiene sin calcular. Si no, muestra el dictamen (cumple / no cumple), Vs, T, Sa, Wt, Q, R, la deriva por nivel frente al límite, el espectro y la FHE |
| 5. Exportar | Copiar o descargar el reporte, fila CSV para la base de datos NSR-10, imprimir o guardar como PDF, guardar el caso en JSON |
| 6. Comparar | **Guardar como alternativa** y ver todas las alternativas lado a lado (deriva máx. X/Y frente al límite, Wt, Vs, Q, R) |

Los botones **Quitar Fv** y **Altura en cm** repiten las pruebas 2 y 3 del Reto 06 sobre el ejemplo del curso.

## Cómo está hecha
- **El cálculo es el mismo `../codigo/nexo_nsr10.py`** que pasó las 3 pruebas y reproduce Excel + SAP2000. La app lo ejecuta en el navegador con [Pyodide](https://pyodide.org) (Python compilado a WebAssembly). No hay una segunda implementación en JavaScript: si el motor cambia, la app usa la versión nueva.
- `index.html` (estructura), `estilos.css` (tema claro y oscuro), `app.js` (formulario, validación, importador, gráficas con Chart.js, alternativas).
- Los datos no salen del computador. Las alternativas se guardan en el navegador (`localStorage`).
- Para publicarla en internet basta un hosting estático que sirva la carpeta del repositorio (por ejemplo GitHub Pages con el repositorio público, Netlify o un servidor de la universidad).

## Archivos que lee
`../codigo/nexo_nsr10.py` (motor), `../codigo/casos/caso1_completo.json` (ejemplo), `../codigo/equipo.json` (nombres). Si se copia la app a otro lugar, basta poner esos archivos junto a `index.html`.
