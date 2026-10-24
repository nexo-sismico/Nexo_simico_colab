"""Genera los dos videos (sin audio, con subtítulos quemados) y sus guiones/SRT.
- Video_prototipo_NSR10.mp4  (≤ 2 min): salidas reales del prototipo para los 3 casos.
- Video_ejecutivo_Nexo_Sismico.mp4 (≤ 5 min): diapositivas + narración como subtítulos.
El equipo puede grabar la voz encima siguiendo los .srt."""
import json, os, re, subprocess, textwrap, glob, shutil, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from rutas import COD, RES, SAL, ENT, RAIZ, fuente

W, H = 1280, 720
OUT = ENT / "Videos"                 # guion y .srt (van a Git)
MP4 = RAIZ / "08 Multimedia"         # videos (fuera de Git)
TMP = tempfile.mkdtemp(prefix="nexo_frames_")
if not shutil.which("ffmpeg"):
    raise SystemExit("Falta ffmpeg en el PATH (Windows: winget install Gyan.FFmpeg).")
SANS, SANSB = fuente("DejaVuSans.ttf"), fuente("DejaVuSans-Bold.ttf")
MONO, MONOB = fuente("DejaVuSansMono.ttf"), fuente("DejaVuSansMono-Bold.ttf")
F = lambda p, s: ImageFont.truetype(p, s)
NAVY, ORANGE, LIGHT, GREEN, RED, AMBER = (30, 42, 51), (228, 87, 46), (237, 240, 243), (46, 139, 87), (192, 57, 43), (242, 165, 65)

def caption(img, text):
    """Barra de subtítulo en la parte inferior."""
    d = ImageDraw.Draw(img, "RGBA")
    f = F(SANS, 26)
    lines = textwrap.wrap(text, 78)[:3]
    h = 24 + 36 * len(lines)
    d.rectangle([0, H - h, W, H], fill=(0, 0, 0, 200))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=f)
        d.text(((W - tw) / 2, H - h + 12 + i * 36), l, font=f, fill=(255, 255, 255))
    return img

def terminal(title, lines, colors=None, cmd=None):
    img = Image.new("RGB", (W, H), (18, 22, 28))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 44], fill=(44, 52, 62))
    for i, c in enumerate([(237, 106, 94), (245, 191, 79), (98, 197, 84)]):
        d.ellipse([18 + i * 26, 14, 34 + i * 26, 30], fill=c)
    d.text((110, 11), title, font=F(SANS, 18), fill=(200, 205, 210))
    y = 62
    if cmd:
        d.text((24, y), "$ ", font=F(MONOB, 20), fill=(98, 197, 84))
        d.text((50, y), cmd, font=F(MONOB, 20), fill=(240, 240, 240)); y += 34
    fm = F(MONO, 18)
    for i, l in enumerate(lines):
        col = (colors or {}).get(i, (215, 220, 225))
        d.text((24, y), l, font=fm, fill=col); y += 25
    return img

def save(img, name):
    p = f"{TMP}/{name}.png"; img.save(p); return p

def render(segs, out_mp4, srt_path):
    """segs = [(png, segundos, texto)] → mp4 + srt."""
    lst = f"{TMP}/{os.path.basename(out_mp4)}.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p, s, _ in segs:
            f.write(f"file '{Path(p).resolve().as_posix()}'\nduration {s:.2f}\n")
        f.write(f"file '{Path(segs[-1][0]).resolve().as_posix()}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-vf", "fps=25,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                    "-movflags", "+faststart", "-t", f"{sum(s for _, s, _ in segs):.2f}", out_mp4], check=True)   # -t: el último cuadro repetido no suma tiempo
    t = 0.0
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (_, s, txt) in enumerate(segs, 1):
            f.write(f"{i}\n{ts(t)} --> {ts(t + s)}\n{txt}\n\n"); t += s
    return t

# --------------------------------------------------------------------------- slides a PNG
PPT_PDF = ENT / "Presentacion" / "Presentacion_Nexo_Sismico.pdf"
if shutil.which("pdftoppm"):
    subprocess.run(["pdftoppm", "-png", "-scale-to-x", str(W), "-scale-to-y", str(H), str(PPT_PDF), f"{TMP}/slide"], check=True)
else:  # Windows sin poppler: pip install pypdfium2
    import pypdfium2
    for i, pg in enumerate(pypdfium2.PdfDocument(str(PPT_PDF)), 1):
        pg.render(scale=W / pg.get_width()).to_pil().save(f"{TMP}/slide-{i:02d}.png")
slides = sorted(glob.glob(f"{TMP}/slide-*.png"))
slide = lambda n: Image.open(slides[n - 1]).convert("RGB").resize((W, H))

# =========================================================================== VIDEO 1: PROTOTIPO
caso1 = json.load(open(COD / "casos/caso1_completo.json", encoding="utf-8"))
r1 = open(RES / "caso1_completo.txt", encoding="utf-8").read().splitlines()
r2 = open(RES / "caso2_falta_dato.txt", encoding="utf-8").read().splitlines()
r3 = open(RES / "caso3_dato_erroneo.txt", encoding="utf-8").read().splitlines()

def seg_txt(s, n=8):
    return s

js = json.dumps({"id": caso1["id"], "sitio": caso1["sitio"], "sistema": caso1["sistema"],
                 "geometria": {k: caso1["geometria"][k] for k in ("Bx", "By", "h_losa", "alturas_libres")},
                 "pesos": caso1["pesos"], "periodos_sap": caso1["periodos_sap"]}, ensure_ascii=False, indent=1)
js_lines = []
for l in js.splitlines():
    js_lines += textwrap.wrap(l, 105, subsequent_indent="    ") or [""]
js_lines = js_lines[:22] + ["  … desplazamientos de 12 combinaciones en las esquinas E5 y A1 …", "}"]

def colorize(lines):
    c = {}
    for i, l in enumerate(lines):
        if "✓" in l or "CUMPLEN" in l or l.startswith("Estado: OK"): c[i] = (120, 220, 140)
        elif "✗" in l or "FALTA" in l or "ERROR" in l or "INVALID" in l: c[i] = (255, 120, 110)
        elif l.startswith("==="): c[i] = (245, 191, 79)
    return c

v1 = []
v1.append((save(caption(slide(5), "Nexo Sísmico estima derivas para comparar alternativas. Este es el módulo NSR-10, que produce respuestas de referencia verificables."), "p01"), 13,
           "Nexo Sísmico estima derivas para comparar alternativas. Este es el módulo NSR-10, que produce respuestas de referencia verificables."))
v1.append((save(caption(terminal("casos/caso1_completo.json", js_lines, {}),
                        "Caso 1: edificio del curso, grupo 1, Piedemonte A (Bogotá). Datos del sitio, geometría, pesos y periodos de SAP2000."), "p02"), 14,
           "Caso 1: edificio del curso, grupo 1, Piedemonte A (Bogotá). Datos del sitio, geometría, pesos y periodos de SAP2000."))
c1 = r1[:20]
v1.append((save(caption(terminal("Terminal", c1, colorize(c1), cmd="python correr_pruebas.py"),
                        "Calcula espectro, cortante basal, fuerzas por piso y derivas de 12 combinaciones con torsión accidental."), "p03"), 13,
           "Calcula espectro, cortante basal, fuerzas por piso y derivas de 12 combinaciones con torsión accidental."))
c1b = r1[:2] + ["…"] + r1[13:]
v1.append((save(caption(terminal("Terminal", c1b, colorize(c1b), cmd="python correr_pruebas.py"),
                        "Vs = 23 250 kN, deriva máxima 0,991 % ≤ 1,0 %, Q = 0,0165, R = 5. Cumple. Tiempo: 0,6 ms."), "p04"), 12,
           "Vs = 23 250 kN, deriva máxima 0,991 % ≤ 1,0 %, Q = 0,0165, R = 5. Cumple. Tiempo: 0,6 ms."))
v1.append((save(caption(slide(8), "Reproduce exactamente el cálculo de referencia hecho con Excel y SAP2000."), "p05"), 14,
           "Reproduce exactamente el cálculo de referencia hecho con Excel y SAP2000."))
c2 = ['  "sitio": {"Aa": 0.15, "Av": 0.20, "Fa": 1.65, "TL": 3.0, ...}   ← sin Fv', ""] + r2
v1.append((save(caption(terminal("Terminal · caso 2", c2, colorize(c2), cmd="python correr_pruebas.py"),
                        "Caso 2: si falta un dato, por ejemplo Fv, se detiene antes de calcular y dice cuál falta."), "p06"), 17,
           "Caso 2: si falta un dato, por ejemplo Fv, se detiene antes de calcular y dice cuál falta."))
c3 = ['  "alturas_libres": [350, 2.5, 2.5, 2.5, 2.5]   ← escrito en centímetros', ""] + [x for l in r3 for x in (textwrap.wrap(l, 105, subsequent_indent="      ") or [""])]
v1.append((save(caption(terminal("Terminal · caso 3", c3, colorize(c3), cmd="python correr_pruebas.py"),
                        "Caso 3: si un dato está mal, como una altura en centímetros, lo rechaza y explica el rango válido."), "p07"), 17,
           "Caso 3: si un dato está mal, como una altura en centímetros, lo rechaza y explica el rango válido."))
csv = open(SAL / "base_datos_NSR10.csv", encoding="utf-8-sig").read().splitlines()
cols = csv[0].split(",")
show = ["id", "norma", "n_pisos", "hn_m", "Lx_m", "Ly_m", "W_total_kN", "Tx_s", "dx_pct", "dy_pct"]
import csv as _csv
rows = list(_csv.DictReader(open(SAL / "base_datos_NSR10.csv", encoding="utf-8-sig")))
def fmt(v):
    try: return f"{float(v):.3f}" if "." in v else v
    except: return v[:14]
tab = ["  ".join(f"{c:>11}" for c in show)] + ["  ".join(f"{fmt(r.get(c, '')):>11}" for c in show) for r in rows]
v1.append((save(caption(terminal("base_datos_NSR10.csv · 19 registros", tab[:21], {0: (245, 191, 79), len(tab) - 1: (120, 220, 140)} if len(tab) <= 21 else {0: (245, 191, 79)}),
                        "Cada caso válido se convierte en un registro de la base de datos NSR-10 que alimenta al predictor."), "p08"), 13,
           "Cada caso válido se convierte en un registro de la base de datos NSR-10 que alimenta al predictor."))
end = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(end)
d.text((90, 250), "Nexo Sísmico · Módulo NSR-10", font=F(SANSB, 52), fill=(255, 255, 255))
d.text((90, 330), "3 pruebas: completa ✓ · falta un dato ✗ · dato erróneo ✗", font=F(SANS, 30), fill=(200, 210, 220))
d.text((90, 380), "Código en el repositorio del equipo (sin claves ni tokens)", font=F(SANS, 26), fill=ORANGE)
v1.append((save(end, "p09"), 5, "Nexo Sísmico · Módulo NSR-10. Código en el repositorio del equipo, sin claves ni tokens."))
dur1 = render(v1, str(MP4 / "Video_prototipo_NSR10.mp4"), OUT / "Video_prototipo_NSR10.srt")

# =========================================================================== VIDEO 2: EJECUTIVO
prs = Presentation(str(ENT / "Presentacion" / "Presentacion_Nexo_Sismico.pptx"))
notes = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else "" for s in prs.slides]
WPS = 2.45  # palabras por segundo (ritmo de lectura en voz alta)
v2 = []
for n, txt in enumerate(notes, 1):
    frases = re.split(r"(?<=[.:;?])\s+", txt.strip())
    # agrupar frases cortas para que cada subtítulo tenga 10–30 palabras
    grupos, cur = [], ""
    for fr in frases:
        if cur and len((cur + " " + fr).split()) > 30:
            grupos.append(cur); cur = fr
        else:
            cur = (cur + " " + fr).strip()
    if cur: grupos.append(cur)
    for k, g in enumerate(grupos):
        dur = max(3.0, len(g.split()) / WPS + 0.6)
        v2.append((save(caption(slide(n), g), f"e{n:02d}_{k}"), dur, g))
dur2 = render(v2, str(MP4 / "Video_ejecutivo_Nexo_Sismico.mp4"), OUT / "Video_ejecutivo_Nexo_Sismico.srt")

# guion legible
with open(OUT / "Guion_video_ejecutivo.md", "w", encoding="utf-8") as f:
    f.write(f"# Guion del video ejecutivo (duración {int(dur2 // 60)}:{int(dur2 % 60):02d})\n\n"
            "Narración por diapositiva. Para grabar la voz: reproducir el MP4 y leer cada subtítulo cuando aparece, "
            "o grabar el audio aparte y montarlo sobre el MP4 (el .srt tiene los tiempos).\n\n")
    t = 0
    titulos = []
    for s in prs.slides:
        tt = [sh.text_frame.text for sh in s.shapes if sh.is_placeholder and sh.placeholder_format.type in (1, 3)]
        titulos.append(tt[0] if tt else "")
    for n, txt in enumerate(notes, 1):
        d_s = sum(s for p, s, _ in v2 if os.path.basename(p).startswith(f"e{n:02d}_"))
        f.write(f"## {n}. {titulos[n-1]}  ·  {int(t // 60)}:{int(t % 60):02d} ({d_s:.0f} s)\n\n{txt}\n\n"); t += d_s
print(f"prototipo: {dur1:.0f} s · ejecutivo: {dur2:.0f} s")
