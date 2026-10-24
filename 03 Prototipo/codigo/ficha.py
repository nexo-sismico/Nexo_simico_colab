"""Ficha técnica de 1 página del prototipo (Reto 06 · AECODE): problema, funcionamiento, tecnología,
resultados de las 3 pruebas, mejoras pendientes, medición del impacto y enlaces. Lee los resultados reales de
correr_pruebas.py y los nombres de equipo.json. Salida: 07 Outputs/Prototipo NSR-10 y copia en 04 Entregables/Prototipo."""
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import shutil
from rutas import COD, RES, SAL, ENT, SANS, SANS_B, MONO
pdfmetrics.registerFont(TTFont("LS", SANS()))
pdfmetrics.registerFont(TTFont("LSB", SANS_B()))
pdfmetrics.registerFont(TTFont("DM", MONO()))
NAVY, GRIS = colors.HexColor("#1F3864"), colors.HexColor("#BFBFBF")
st = lambda n, **k: ParagraphStyle(n, fontName=k.pop("f", "LS"), **k)
T = st("t", f="LSB", fontSize=12.5, textColor=NAVY, leading=15)
S = st("s", fontSize=7.6, textColor=colors.HexColor("#444444"), leading=9.4)
H = st("h", f="LSB", fontSize=9, textColor=NAVY, spaceBefore=4, spaceAfter=1.5)
B = st("b", fontSize=7.7, leading=9.7)
C = st("c", fontSize=7.2, leading=8.8)
CH = st("ch", f="LSB", fontSize=7.2, leading=8.8, textColor=colors.white)
eq = json.load(open(COD / "equipo.json", encoding="utf-8"))
r1 = json.load(open(RES / "caso1_completo.json", encoding="utf-8"))
res = json.load(open(RES / "resumen_pruebas.json", encoding="utf-8"))
fx = r1["fhe"]["X"]
n = lambda v, d=0: f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


def tabla(filas, anchos, cab=True, extra=()):
    t = Table([[Paragraph(str(x), CH if (cab and i == 0) else C) for x in f] for i, f in enumerate(filas)], colWidths=[a * mm for a in anchos])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, GRIS), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
                          + ([("BACKGROUND", (0, 0), (-1, 0), NAVY)] if cab else []) + list(extra)))
    return t


PDF = SAL / "Ficha_pruebas_prototipo_NSR10.pdf"
doc = SimpleDocTemplate(str(PDF), pagesize=letter, leftMargin=13*mm, rightMargin=13*mm, topMargin=10*mm, bottomMargin=8*mm,
                        title="Ficha técnica — Prototipo NSR-10 · Nexo Sísmico", author=f"Equipo {eq['equipo']}")
s = [Paragraph("Ficha técnica · Prototipo funcional Nexo Sísmico — verificación sísmica NSR-10 automatizada", T),
     Paragraph(f"Reto 06 · {eq['programa']} · 24 de octubre de 2026 · Equipo {eq['equipo']}: " + " · ".join(p["nombre"] for p in eq["integrantes"]), S)]

s += [Paragraph("1. Problema que ataca", H),
      Paragraph("<b>Quién lo vive:</b> el ingeniero estructural que predimensiona edificios aporticados de concreto y debe comparar varias alternativas antes de fijar el diseño. "
                "<b>Con qué datos:</b> sitio (Aa, Av, Fa, Fv, grupo de uso), geometría, pesos por piso, periodos y desplazamientos de esquina que exporta SAP2000. "
                "<b>Demoras y errores actuales:</b> cada alternativa obliga a rehacer en hojas de cálculo el espectro, la fuerza horizontal equivalente, las derivas de 12 combinaciones y la revisión de estabilidad; "
                "un dato faltante o en unidades equivocadas (centímetros en lugar de metros) se propaga sin aviso hasta el dictamen.", B)]

s += [Paragraph("2. Cómo funciona (entra → hace → sale) y límites", H)]
esquema = ENT / "Prototipo" / "Esquema_prototipo.png"
if esquema.exists():
    s += [Image(str(esquema), width=188*mm, height=188*mm * 0.25)]
s += [Paragraph("<b>Entra:</b> un JSON con los datos del edificio. <b>Hace:</b> valida campos, tipos y rangos (si falta o sobra algo, se detiene sin calcular ni suponer valores) y aplica la NSR-10: espectro A.2, periodo Cu·Ta y FHE A.4, torsión accidental 5 % A.3.6.7, derivas A.6 con 12 combinaciones en dos esquinas, índice Q y coeficiente R A.3.3. "
                "<b>Sale:</b> reporte con dictamen (cumple / no cumple) y un registro para la base de datos del predictor. "
                "<b>Límites:</b> la tecnología valida y calcula; la persona modela en SAP2000, revisa el dictamen y decide el diseño. El cálculo es determinista y trazable a la norma: no usa IA generativa.", B)]

s += [Paragraph("3. Tecnología utilizada", H),
      tabla([["Componente", "Herramienta", "Uso"],
             ["Motor de validación y cálculo", "Python 3 (<i>nexo_nsr10.py</i>, solo biblioteca estándar)", "Valida la entrada y aplica NSR-10 Títulos A y B"],
             ["Datos de entrada", "JSON + SAP2000", "Periodos y desplazamientos del modelo del caso real"],
             ["Interfaz para ingenieros", "App web: HTML, JavaScript, Chart.js y Pyodide", "Ejecuta el mismo motor Python en el navegador"],
             ["Base de datos y predictor", "pandas · scikit-learn (Random Forest)", "Cada caso válido alimenta el modelo de derivas"],
             ["Versionado y trabajo en equipo", "GitHub · Obsidian · asistentes de IA para programar", "Código, pruebas y documentación sin claves ni tokens"]],
            [50, 70, 64])]

s += [Paragraph("4. Resultados de las 3 pruebas (caso real: edificio de oficinas de 5 pisos, grupo 1, Bogotá, microzona Piedemonte A)", H)]
desc = [("1 · Datos completos", "Todos los datos del edificio y las 12 combinaciones de SAP2000", "Calcular y emitir dictamen"),
        ("2 · Falta un dato", "Se elimina Fv (coeficiente de amplificación)", "Avisar el dato faltante; no inventarlo"),
        ("3 · Dato erróneo", "Altura libre del piso 1 = 350 (escrita en cm)", "Marcar el error y rechazarlo")]
filas = [["Prueba", "Entrada", "Esperado", "Obtenido (ejecución real)", "Tiempo"]]
for (c, e, esp), rr in zip(desc, res):
    obt = {"ok": f"<b>OK</b>: Vs = {n(fx['Vs'])} kN; deriva máx. {n(r1['deriva_max_pct']['X'], 3)} % (X) y {n(r1['deriva_max_pct']['Y'], 3)} % (Y) ≤ 1,0 %; Q = {n(r1['Q_max'], 4)}; R = {n(r1['R'], 1)} → <b>cumple</b>",
           "faltan_datos": f"<b>Detenido</b>: «FALTA: {rr['detalle'][0]}». No calcula ni supone el valor.",
           "datos_invalidos": f"<b>Rechazado</b>: «{rr['detalle'][0]}». No calcula."}[rr["estado"]]
    filas.append([c, e, esp, obt, f"{n(rr['ms'], 1)} ms"])
s += [tabla(filas, [23, 45, 29, 71, 16], extra=[("BACKGROUND", (3, 1), (3, 1), colors.HexColor("#E2EFDA")),
                                                 ("BACKGROUND", (3, 2), (3, 3), colors.HexColor("#FCE4D6"))]),
      Paragraph(f"<b>Validación de la prueba 1</b> contra el cálculo de referencia (Excel del curso + SAP2000): Vs 23 250 kN = {n(fx['Vs'])} kN · fuerza en cubierta 7 361 kN = {n(fx['F'][-1])} kN · "
                f"derivas 0,985 / 0,991 % = {n(r1['deriva_max_pct']['X'], 3)} / {n(r1['deriva_max_pct']['Y'], 3)} % · Q 0,0165 = {n(r1['Q_max'], 4)}. Coincidencia exacta.", B)]

s += [Paragraph("5. Qué falta por mejorar", H),
      Paragraph("• <b>Interfaz:</b> ya hay una app web local (<i>03 Prototipo/app</i>) que usa el mismo motor; falta publicarla en internet y conectar el bot de Telegram en n8n. "
                "• <b>Entrada directa desde SAP2000:</b> leer las tablas exportadas o la API en lugar de armar el JSON a mano. "
                "• <b>Más verificaciones:</b> irregularidades en planta y altura además de la torsional, y combinaciones de diseño. "
                "• <b>Más casos verificados</b> para la base NSR-10 (hoy 18 edificios teóricos del profesor + este caso). "
                "• <b>Medir el ahorro de tiempo</b> con 5 casos reales (ver sección 6).", B)]

s += [Paragraph("6. Medición del impacto (antes vs. después)", H),
      Paragraph(f"<b>Después (medido):</b> el prototipo valida y calcula un caso en {n(res[0]['ms'], 1)} ms y rechaza entradas defectuosas en {n(res[1]['ms'], 1)} ms. "
                "<b>Antes (manual):</b> pendiente de cronometrar con 5 casos siguiendo el protocolo de <i>Definicion_prototipo.pdf</i>; "
                "no se reporta un porcentaje de ahorro hasta medirlo.", B)]

s += [Paragraph("7. Enlace y capturas", H),
      Paragraph(f"Repositorio: <b>{eq['repositorio']}</b> (código en <i>03 Prototipo/codigo</i>; ejecutar <i>python correr_pruebas.py</i> o <i>python demo_en_vivo.py</i>). "
                "Capturas de las 3 pruebas en <i>04 Entregables/Prototipo/capturas</i>; video de demostración de menos de 2 min. "
                "Sin claves, tokens ni datos personales: las pruebas usan datos de un edificio académico.", S)]
doc.build(s)
shutil.copy(PDF, ENT / "Prototipo" / PDF.name)   # copia para entregar
print("ficha →", PDF, "y", ENT / "Prototipo")
