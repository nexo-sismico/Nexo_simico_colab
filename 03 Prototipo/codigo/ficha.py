import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Preformatted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import shutil
from rutas import RES, SAL, ENT, SANS, SANS_B, MONO
pdfmetrics.registerFont(TTFont("LS", SANS()))
pdfmetrics.registerFont(TTFont("LSB", SANS_B()))
pdfmetrics.registerFont(TTFont("DM", MONO()))
NAVY = colors.HexColor("#1F3864")
st = lambda n, **k: ParagraphStyle(n, fontName=k.pop("f", "LS"), **k)
T = st("t", f="LSB", fontSize=13, textColor=NAVY, leading=16)
S = st("s", fontSize=8, textColor=colors.HexColor("#555555"), leading=10)
H = st("h", f="LSB", fontSize=9.5, textColor=NAVY, spaceBefore=5, spaceAfter=2)
B = st("b", fontSize=8, leading=10.3)
C = st("c", fontSize=7.4, leading=9)
CH = st("ch", f="LSB", fontSize=7.4, leading=9, textColor=colors.white)
M = st("m", f="DM", fontSize=6.3, leading=7.6)
r1 = json.load(open(RES / "caso1_completo.json", encoding="utf-8"))
res = json.load(open(RES / "resumen_pruebas.json", encoding="utf-8"))
PDF = SAL / "Ficha_pruebas_prototipo_NSR10.pdf"
doc = SimpleDocTemplate(str(PDF), pagesize=letter, leftMargin=14*mm, rightMargin=14*mm,
                        topMargin=11*mm, bottomMargin=10*mm, title="Ficha de pruebas — Prototipo NSR-10")
s = [Paragraph("Ficha de pruebas · Prototipo Nexo Sísmico – Módulo NSR-10", T),
     Paragraph("Beca AI Talent (AECODE) · Investigación académica aplicada · Responsable del módulo: Nicolás Infante · 24 de octubre de 2026", S),
     Paragraph("Qué es el prototipo", H),
     Paragraph("Automatización en Python que recibe los datos de un edificio aporticado de concreto (JSON), <b>valida</b> que estén completos y en rango, "
               "y calcula según NSR-10: espectro y Sa, periodo con límite Cu·Ta, cortante basal y fuerzas por piso con torsión accidental (FHE), "
               "derivas con la envolvente de 12 combinaciones (±F, ±Mz) en dos esquinas, índice de estabilidad Q y coeficiente R. "
               "Genera además un registro para la base de datos que alimentará el modelo de aprendizaje automático. "
               "Caso de prueba: edificio de oficinas de 5 pisos del curso (grupo 1, Bogotá, microzona Piedemonte A) con resultados de SAP2000.", B),
     Paragraph("Pruebas", H)]
rows = [[Paragraph(x, CH) for x in ["Caso", "Entrada", "Resultado esperado", "Resultado obtenido", "Tiempo"]]]
desc = [("1 · Bien llenado", "Todos los datos del edificio (sitio, pesos, periodos, desplazamientos de 12 combinaciones)",
         "Cálculo completo y dictamen"),
        ("2 · Falta un dato", "Se elimina Fv (coeficiente de amplificación)", "Detener y pedir el dato faltante"),
        ("3 · Dato equivocado", "Altura libre del piso 1 = 350 (en cm, no en m)", "Rechazar el valor e indicar el rango")]
for (c, e, esp), rr in zip(desc, res):
    ok = rr["estado"]
    obt = {"ok": f"<b>OK</b>: {rr['detalle'][0]}; cumple 1.0 % hpi; Q máx = {r1['Q_max']:.3f}; R = {r1['R']:.1f}",
           "faltan_datos": "<b>Detenido</b>: 'FALTA: sitio.Fv — coeficiente de amplificación Fv'",
           "datos_invalidos": "<b>Rechazado</b>: 'altura libre nivel 1 = 350 m fuera de [1.8, 6.0] m — ¿está en cm?'"}[ok]
    rows.append([Paragraph(c, C), Paragraph(e, C), Paragraph(esp, C), Paragraph(obt, C), Paragraph(f"{rr['ms']} ms", C)])
t = Table(rows, colWidths=[24*mm, 50*mm, 32*mm, 66*mm, 14*mm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
                       ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (3, 1), (3, 1), colors.HexColor("#E2EFDA")),
                       ("BACKGROUND", (3, 2), (3, 3), colors.HexColor("#FCE4D6"))]))
s += [t, Paragraph("Validación contra el cálculo de referencia (Excel del curso + SAP2000)", H)]
fx = r1["fhe"]["X"]
val = [["Magnitud", "Referencia (Excel)", "Prototipo"],
       ["Cortante basal Vs (kN)", "23 250", f"{fx['Vs']:,.0f}".replace(",", " ")],
       ["Fuerza en cubierta Fx (kN)", "7 361", f"{fx['F'][-1]:,.0f}".replace(",", " ")],
       ["Deriva máx. X / Y (% hpi)", "0.985 / 0.991", f"{r1['deriva_max_pct']['X']:.3f} / {r1['deriva_max_pct']['Y']:.3f}"],
       ["Índice de estabilidad Q máx", "0.0165", f"{r1['Q_max']:.4f}"]]
tv = Table([[Paragraph(x, CH if i == 0 else C) for x in r] for i, r in enumerate(val)], colWidths=[62*mm, 40*mm, 40*mm])
tv.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF"))]))
s += [tv, Paragraph("Captura de la salida (caso 1, extracto)", H)]
txt = open(RES / "caso1_completo.txt", encoding="utf-8").read().splitlines()
s += [Preformatted("\n".join(txt[1:6] + txt[13:20] + txt[-4:-1]), M)]
s += [Paragraph("Conclusión", H),
      Paragraph("El prototipo reproduce el cálculo de referencia y bloquea entradas incompletas o erróneas antes de calcular. "
                "Las derivas del caso quedan a menos de 2 % del límite (0.991 % vs 1.0 %), lo que justifica usar la herramienta para comparar alternativas. "
                "Siguiente paso: alimentar la base de datos NSR-10 (18 edificios del Prof. T. F. Rojas Vallejo + este caso) y conectarla al predictor y al bot. <i>Nota del profesor: varios de esos 18 resultados son teóricos (algunas plantas y luces no se resolverían con pórticos resistentes a momento en la práctica) y las plantas ausentes fallaron en el dimensionamiento del algoritmo de OpenSees; por eso se usan solo para entrenar y comparar, no como diseños.</i>", B),
      Paragraph("Enlace: https://github.com/FrailM7/nexo-sismico · carpeta 03 Prototipo/codigo · sin claves ni tokens.", S)]
doc.build(s)
shutil.copy(PDF, ENT / "Prototipo" / PDF.name)   # copia para entregar
print("ficha →", PDF, "y", ENT / "Prototipo")
