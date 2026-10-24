"""Documentos del Reto 06 (prototipo funcional) que acompañan a la ficha:
  - Esquema_prototipo.png : flujo entra → hace → sale, herramientas y límites tecnología / persona (para Miro y la ficha)
  - Definicion_prototipo.pdf : pieza seleccionada, problema AEC, esquema, herramientas, límites, protocolo de pruebas
    con resultados reales, capturas y plantilla de medición antes/después (sin cifras inventadas).
Salidas en 04 Entregables/Prototipo. Correr después de correr_pruebas.py y antes de ficha.py."""
import json
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rutas import COD, RES, ENT, SANS, SANS_B

OUT = ENT / "Prototipo"
CAP = OUT / "capturas"
eq = json.load(open(COD / "equipo.json", encoding="utf-8"))
res = json.load(open(RES / "resumen_pruebas.json", encoding="utf-8"))
r1 = json.load(open(RES / "caso1_completo.json", encoding="utf-8"))

# ------------------------------------------------------------------ esquema
NAVY, ORANGE, GREEN, RED, GREY = "#1F3864", "#E07B39", "#3A7D44", "#C0392B", "#6B6B6B"
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(12, 3.0)); ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off")


def caja(x, y, w, h, txt, borde, fondo="white", fs=8.6, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.08", fc=fondo, ec=borde, lw=1.4))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color="#1E1E1E", weight=peso, linespacing=1.25)


def flecha(x1, y1, x2, y2, c=GREY):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3))


caja(0.1, 1.15, 2.1, 1.1, "ENTRA\nJSON del edificio:\nsitio, geometría, pesos,\nperiodos y desplazamientos\nde SAP2000", NAVY, "#EEF2F8")
caja(2.75, 1.15, 2.2, 1.1, "1 · VALIDAR\ncampos, tipos, rangos\ny consistencia\n(12 combinaciones)", ORANGE, "#FDF1E8", peso="bold")
caja(5.5, 1.15, 2.6, 1.1, "2 · CALCULAR NSR-10\nespectro A.2 · Cu·Ta y FHE A.4\ntorsión 5 % A.3.6.7\nderivas A.6 · Q · R A.3.3", ORANGE, "#FDF1E8", peso="bold")
caja(8.65, 1.15, 3.25, 1.1, "SALE\nreporte con dictamen\n(cumple / no cumple)\n+ registro para la base\nde datos del predictor", GREEN, "#EAF4EC")
caja(2.75, 0.05, 2.2, 0.7, "falta o error → se detiene,\ndice qué corregir, no calcula", RED, "#FBEAEA", fs=8)
flecha(2.2, 1.7, 2.75, 1.7); flecha(4.95, 1.7, 5.5, 1.7); flecha(8.1, 1.7, 8.65, 1.7); flecha(3.85, 1.15, 3.85, 0.75, RED)
ax.text(0.1, 2.72, "Decide la persona: modela en SAP2000 y prepara la entrada", fontsize=8.5, color=NAVY, weight="bold")
ax.text(2.75, 2.42, "Decide la tecnología (Python, determinista, trazable a la norma)", fontsize=8.5, color=ORANGE, weight="bold")
ax.text(8.65, 2.72, "Decide la persona: revisa el dictamen y\naprueba o cambia la alternativa", fontsize=8.5, color=GREEN, weight="bold", va="center")
ax.text(5.5, 0.35, "Herramientas: Python 3 · JSON · SAP2000 · NSR-10 (Títulos A y B) · scikit-learn (base del predictor) · GitHub", fontsize=8, color=GREY)
plt.tight_layout(pad=0.2); plt.savefig(OUT / "Esquema_prototipo.png", dpi=220); plt.close()

# ------------------------------------------------------------------ documento
pdfmetrics.registerFont(TTFont("LS", SANS())); pdfmetrics.registerFont(TTFont("LSB", SANS_B()))
st = lambda n, **k: ParagraphStyle(n, fontName=k.pop("f", "LS"), **k)
T = st("t", f="LSB", fontSize=14, textColor=colors.HexColor(NAVY), leading=17)
S = st("s", fontSize=8.5, textColor=colors.HexColor("#444444"), leading=11)
H = st("h", f="LSB", fontSize=10.5, textColor=colors.HexColor(NAVY), spaceBefore=7, spaceAfter=3)
B = st("b", fontSize=9, leading=12)
C = st("c", fontSize=8.3, leading=10.4)
CH = st("ch", f="LSB", fontSize=8.3, leading=10.4, textColor=colors.white)
n = lambda v, d=0: f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


def tabla(filas, anchos):
    t = Table([[Paragraph(str(x), CH if i == 0 else C) for x in f] for i, f in enumerate(filas)], colWidths=[a * mm for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return t


def captura(nombre, ancho=180):
    p = CAP / nombre
    if not p.exists():
        return Paragraph(f"(falta la captura {nombre}: correr demo_en_vivo.py y extraerla)", S)
    from PIL import Image as PI
    w, h = PI.open(p).size
    return Image(str(p), width=ancho * mm, height=ancho * mm * h / w)


doc = SimpleDocTemplate(str(OUT / "Definicion_prototipo.pdf"), pagesize=letter, leftMargin=16*mm, rightMargin=16*mm, topMargin=13*mm, bottomMargin=12*mm,
                        title="Definición del prototipo funcional — Nexo Sísmico", author=f"Equipo {eq['equipo']}")
s = [Paragraph("Definición del prototipo funcional — Nexo Sísmico", T),
     Paragraph(f"Reto 06 · {eq['programa']} · 24 de octubre de 2026<br/>Equipo: " + " · ".join(p["nombre"] for p in eq["integrantes"]), S),
     Paragraph("1. Pieza tecnológica seleccionada", H),
     Paragraph("Del proyecto final (estimación de derivas sísmicas con generación paramétrica, verificación normativa y Random Forest) se eligió el "
               "<b>módulo de verificación sísmica NSR-10</b>: recibe los datos de un edificio aporticado de concreto, los valida y calcula el análisis sísmico "
               "hasta las derivas y el dictamen. Es la pieza que produce respuestas de referencia confiables y registros para la base de datos del predictor, "
               "y se puede probar de punta a punta con un caso real.", B),
     Paragraph("2. Problema AEC", H),
     tabla([["Pregunta", "Respuesta"],
            ["¿Quién vive el problema?", "El ingeniero estructural que predimensiona edificios aporticados y compara alternativas (luces, secciones, alturas)."],
            ["¿Con qué datos trabaja?", "Parámetros del sitio (Aa, Av, Fa, Fv, grupo de uso), geometría, pesos por piso, periodos y desplazamientos de esquina exportados de SAP2000 para 12 combinaciones."],
            ["¿Qué demoras genera hoy?", "Cada alternativa obliga a rehacer en hojas de cálculo el espectro, la fuerza horizontal equivalente, la torsión accidental, las derivas y la revisión de estabilidad."],
            ["¿Qué errores genera hoy?", "Un dato faltante o en otras unidades (por ejemplo, una altura en centímetros) se propaga sin aviso hasta el dictamen; las fórmulas copiadas entre hojas se desalinean."]],
           [45, 136]),
     Paragraph("3. Esquema de funcionamiento (entra → hace → sale) y límites", H),
     Image(str(OUT / "Esquema_prototipo.png"), width=182*mm, height=182*mm * 0.25),
     tabla([["Decide la tecnología", "Requiere decisión humana"],
            ["Si la entrada está completa, en rango y es consistente; si no, se detiene y explica qué corregir.",
             "Construir el modelo en SAP2000 (geometría, secciones, cargas) y exportar los resultados."],
            ["Los cálculos normativos (espectro, Cu·Ta, FHE, torsión, derivas, Q, R) y el dictamen de derivas.",
             "Revisar el dictamen, interpretar casos cercanos al límite y decidir la alternativa de diseño."],
            ["El registro del caso para la base de datos.", "Aprobar el diseño final: el prototipo no sustituye la verificación profesional."]],
           [90.5, 90.5]),
     Paragraph("4. Herramientas", H),
     Paragraph("Python 3 (<i>nexo_nsr10.py</i>, solo biblioteca estándar) para validar y calcular; JSON como formato de entrada; SAP2000 como fuente de periodos y desplazamientos; "
               "NSR-10 Títulos A y B como reglas; pandas y scikit-learn para la base de datos del predictor; GitHub y Obsidian para el trabajo en equipo; "
               "asistentes de IA para programar y documentar. El cálculo no usa IA generativa: es determinista y trazable.", B),
     PageBreak(),
     Paragraph("5. Protocolo de pruebas y resultados (ejecución real, no simulada)", H)]
desc = [("1 · Camino feliz", "Edificio de oficinas de 5 pisos del curso (grupo 1, Bogotá, Piedemonte A), datos completos", "Calcular y dar la respuesta correcta"),
        ("2 · Dato faltante", "Mismo edificio sin Fv (coeficiente de amplificación)", "Avisar que falta el dato; no inventarlo"),
        ("3 · Dato erróneo", "Altura libre del piso 1 = 350 (en centímetros, imposible en metros)", "Marcarlo como error y rechazarlo")]
filas = [["Prueba", "Entrada", "Esperado", "Obtenido", "Tiempo"]]
fx = r1["fhe"]["X"]
for (c, e, esp), rr in zip(desc, res):
    obt = {"ok": f"OK: Vs = {n(fx['Vs'])} kN, derivas {n(r1['deriva_max_pct']['X'], 3)} / {n(r1['deriva_max_pct']['Y'], 3)} % ≤ 1,0 %, Q = {n(r1['Q_max'], 4)}, R = {n(r1['R'], 1)}: cumple. Igual al cálculo de referencia (Excel + SAP2000).",
           "faltan_datos": f"Detenido: «FALTA: {rr['detalle'][0]}». No calcula.",
           "datos_invalidos": f"Rechazado: «{rr['detalle'][0]}». No calcula."}[rr["estado"]]
    filas.append([c, e, esp, obt, f"{n(rr['ms'], 1)} ms"])
s += [tabla(filas, [23, 42, 30, 70, 17]),
      Paragraph("Capturas de la grabación en vivo (consola de Windows, <i>python demo_en_vivo.py</i>):", S),
      KeepTogether([captura("prueba2_falta_dato.png", 138), captura("prueba3_dato_erroneo.png", 138), captura("resumen_3_pruebas.png", 138)]),
      Paragraph("La captura completa de la prueba 1 está en <i>capturas/prueba1_datos_completos.png</i>; el video <i>Video_prototipo_en_vivo.mp4</i> muestra la ejecución completa.", S),
      Paragraph("6. Medición del impacto (antes vs. después) — plantilla para 5 casos", H),
      Paragraph("Método: la misma persona prepara cada caso desde los resultados de SAP2000 y cronometra (a) el cálculo manual en la hoja de cálculo hasta el dictamen de derivas y "
                "(b) el llenado del JSON más la ejecución del prototipo. Se reportan solo tiempos medidos; los campos vacíos se completan al cronometrar.", B),
      tabla([["Caso", "Tiempo manual (min)", "Tiempo con el prototipo (min)", "Cálculo del prototipo", "Errores detectados"],
             ["1 · Edificio del curso, grupo 1", "", "", f"{n(res[0]['ms'], 1)} ms (medido)", "—"],
             ["2", "", "", "", ""], ["3", "", "", "", ""], ["4", "", "", "", ""], ["5", "", "", "", ""]],
            [52, 32, 40, 32, 26]),
      Paragraph("7. Reglas cumplidas", H),
      Paragraph("<b>Seguridad:</b> sin claves, tokens ni contraseñas en código, capturas o video (la sincronización del repositorio bloquea patrones de claves). "
                "<b>Privacidad:</b> las pruebas usan un edificio académico, sin datos personales. "
                f"<b>Veracidad:</b> todos los resultados provienen de ejecuciones reales y están en el repositorio ({eq['repositorio']}).", B)]
doc.build(s)
print("→", OUT / "Esquema_prototipo.png", "·", OUT / "Definicion_prototipo.pdf")
