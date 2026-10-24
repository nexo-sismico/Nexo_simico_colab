"""Configuración única del proyecto: plantas, pisos, uso y avalúo de cargas según NSR-10 Título B."""
import math

H_ENTREPISO = 3.0  # m

PLANTAS = [
    ("P1",  [5.0]*3,                [5.0]*3,               "Cuadrada, luces medias"),
    ("P2",  [4.5]*5,                [6.0]*3,               "Rectangular, vanos cortos en X"),
    ("P3",  [7.0, 4.0, 7.0],        [5.0]*4,               "Pasillo central"),
    ("P4",  [6.0]*4,                [6.0]*4,               "Cuadrada, 4x4 vanos"),
    ("P5",  [7.0]*4,                [6.5]*3,               "Rectangular horizontal"),
    ("P6",  [4.0]*5,                [4.0]*4,               "Muchos vanos cortos"),
    ("P7",  [8.0]*4,                [8.0]*4,               "Cuadrada, luces largas"),
    ("P8",  [5.0, 7.0, 7.0, 5.0],   [6.0, 4.0, 6.0],       "Luces variables"),
    ("P9",  [6.0]*3,                [8.0]*2,               "Vanos rectangulares"),
    ("P10", [8.0]*3,                [5.0]*5,               "Vanos rectangulares"),
]

PISOS = {
    "P1": (8, 10), "P2": (6, 10), "P3": (4, 6), "P4": (6, 8), "P5": (4, 8),
    "P6": (6, 10), "P7": (4, 6), "P8": (4, 8), "P9": (4, 10), "P10": (8, 10),
}

# ---- Losa aligerada en una dirección con casetón de poliestireno (igual criterio para todas) ----
LOSA = dict(hls=0.05, bvt=0.12, Sv=0.70, g_c=24.0, g_p=0.2, div=18.5)
# hls: loseta superior (NSR-10 C.8.13.6: >= 45 mm) | bvt: ancho de vigueta (C.8.13.2: >= 100 mm)
# Sv: separación c-c de viguetas (C.8.13.3: separación libre <= 2.5 h y <= 1.20 m)
# g_c: concreto reforzado 24 kN/m3 (Tabla B.3.2-1) | g_p: poliestireno del casetón (dato del equipo)
# h = L/18.5 redondeado a 0.05 m (Tabla C.9.5(a), losa nervada en una dirección, un extremo continuo)

# ---- Uso y cargas por planta (valores tomados de las tablas de NSR-10 Título B) ----
# pisos: Tabla B.3.4.1-3 | cielo y ductos: Tabla B.3.4.1-1 | muros: Tabla B.3.4.3-1 ("Fachada y particiones")
# imper: Tabla B.3.4.1-4 | afinado de cubierta: Tabla B.3.4.1-3 | L: Tabla B.4.2.1-1 | Lc: Tabla B.4.2.1-2
AFINADO_CUB = ("Afinado de 25 mm sobre concreto de agregado pétreo", 1.50)
USO = {
    "P1": dict(uso="Residencial multifamiliar", grupo="I", I=1.00, Lv=5.0,
               pisos=("Baldosa cerámica de 20 mm sobre mortero de 25 mm", 1.10),
               cielo=("Pañete en yeso o concreto", 0.25), ductos=0.0,
               muros=("Residencial - fachada y particiones de mampostería", 3.0),
               imper=("Tela asfáltica", 0.03), terraza=None,
               L=("Residencial - cuartos privados y sus corredores", 1.8),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 1.8)),
    "P2": dict(uso="Hotel", grupo="I", I=1.00, Lv=4.5,
               pisos=("Mármol y mortero sobre concreto de agregado pétreo", 1.60),
               cielo=("Entramado metálico suspendido afinado en yeso", 0.50), ductos=0.20,
               muros=("Residencial - fachada y particiones livianas", 2.0),
               imper=("Membrana de líquido aplicado", 0.05),
               terraza=("Baldosa cerámica de 20 mm sobre mortero de 25 mm", 1.10),
               L=("Residencial - cuartos privados y sus corredores", 1.8),
               Lc=("Terraza de uso público: la del uso (Reunión - silletería móvil, Tabla B.4.2.1-1)", 5.0)),
    "P3": dict(uso="Colegio", grupo="III", I=1.25, Lv=5.0,
               pisos=("Terrazzo de 25 mm sobre concreto de 50 mm o sobre afinado", 1.50),
               cielo=("Pañete en yeso o concreto", 0.25), ductos=0.20,
               muros=("Educativos - salones de clase", 2.0),
               imper=("Membrana bituminosa lisa", 0.10), terraza=None,
               L=("Educativos: salones 2.0 y corredores 5.0, ponderado por área (14 m aulas + 4 m pasillo)", 2.7),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación (valor ponderado)", 2.7)),
    "P4": dict(uso="Centro comercial", grupo="II", I=1.10, Lv=6.0,
               pisos=("Terrazzo de 40 mm directamente sobre la losa", 0.90),
               cielo=("Entramado metálico suspendido afinado en yeso", 0.50), ductos=0.20,
               muros=("Comercio - exhibición y venta de mercancías", 1.5),
               imper=("Membrana bituminosa con grava", 0.25), terraza=None,
               L=("Comercio - minorista", 5.0),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 5.0)),
    "P5": dict(uso="Oficinas", grupo="I", I=1.00, Lv=6.5,
               pisos=("Afinado de 25 mm sobre concreto de agregado pétreo", 1.50),
               cielo=("Entramado metálico suspendido afinado en cemento", 0.70), ductos=0.20,
               muros=("Oficinas - particiones fijas de mampostería", 2.0),
               imper=("Membrana bituminosa lisa", 0.10), terraza=None,
               L=("Oficinas - oficinas", 2.0),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 2.0)),
    "P6": dict(uso="Residencial (apartamentos pequeños)", grupo="I", I=1.00, Lv=4.0,
               pisos=("Baldosa cerámica de 20 mm sobre mortero de 12 mm", 0.80),
               cielo=("Pañete en yeso o concreto", 0.25), ductos=0.0,
               muros=("Residencial - fachada y particiones de mampostería", 3.0),
               imper=("Tela asfáltica", 0.03), terraza=None,
               L=("Residencial - cuartos privados y sus corredores", 1.8),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 1.8)),
    "P7": dict(uso="Comercio mayorista", grupo="II", I=1.10, Lv=8.0,
               pisos=("Afinado de 25 mm sobre concreto de agregado pétreo", 1.50),
               cielo=("Sin cielo raso (instalaciones a la vista)", 0.0), ductos=0.20,
               muros=("Comercio - exhibición y venta de mercancías", 1.5),
               imper=("Membrana bituminosa con grava", 0.25), terraza=None,
               L=("Comercio - mayorista", 6.0),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 6.0)),
    "P8": dict(uso="Clínica / hospital", grupo="IV", I=1.50, Lv=6.0,
               pisos=("Afinado de 25 mm (1.50) + piso asfáltico o linóleo de 6 mm (0.05)", 1.55),
               cielo=("Entramado metálico suspendido afinado en cemento", 0.70), ductos=0.20,
               muros=("Institucional - internados con atención a residentes", 2.0),
               imper=("Membrana bituminosa lisa", 0.10), terraza=None,
               L=("Institucional: cirugía y laboratorios 4.0 (franja 6 m), corredor 5.0 (franja central 4 m) y cuartos privados 2.0 (franja 6 m), ponderado por área", 3.5),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación (valor ponderado)", 3.5)),
    "P9": dict(uso="Universidad", grupo="III", I=1.25, Lv=6.0,
               pisos=("Baldosa sobre mortero de 25 mm", 1.10),
               cielo=("Entramado metálico suspendido afinado en yeso", 0.50), ductos=0.20,
               muros=("Educativos - salones de clase", 2.0),
               imper=("Membrana de líquido aplicado", 0.05), terraza=None,
               L=("Educativos - salones de clase", 2.0),
               Lc=("Cubiertas, azoteas y terrazas: la misma del resto de la edificación", 2.0)),
    "P10": dict(uso="Oficinas", grupo="I", I=1.00, Lv=5.0,
                pisos=("Baldosa cerámica de 20 mm sobre mortero de 25 mm", 1.10),
                cielo=("Tableros de yeso de 12 mm (0.0080 kN/m² por mm)", 0.10), ductos=0.20,
                muros=("Oficinas - particiones móviles de altura total", 1.0),
                imper=("Membrana de líquido aplicado", 0.05),
                terraza=("Baldosa cerámica de 20 mm sobre mortero de 25 mm", 1.10),
                L=("Oficinas - oficinas", 2.0),
                Lc=("Terraza de uso público: la del uso (Reunión - silletería móvil, Tabla B.4.2.1-1)", 5.0)),
}


# Luz de viguetas: se arman en la dirección de menor luz -> menor de las luces máximas en X y en Y
for _pid, _sx, _sy, _ in PLANTAS:
    USO[_pid]["Lv"] = min(max(_sx), max(_sy))

REL_ASPECTO_MAX = 1.5  # criterio del equipo para limitar efectos torsionales
for _pid, _sx, _sy, _ in PLANTAS:
    _r = max(sum(_sx), sum(_sy)) / min(sum(_sx), sum(_sy))
    assert _r <= REL_ASPECTO_MAX + 1e-9, f"{_pid}: relación de aspecto {_r:.2f} > {REL_ASPECTO_MAX}"


def losa(pid):
    p = LOSA
    Lv = USO[pid]["Lv"]
    h = math.ceil(round(Lv / p["div"] / 0.05, 6)) * 0.05
    hcas = h - p["hls"]
    SL = p["Sv"] - p["bvt"]
    loseta = p["g_c"] * p["hls"]
    vig = p["g_c"] * p["bvt"] * hcas / p["Sv"]
    cas = p["g_p"] * hcas * SL / p["Sv"]
    return dict(h=round(h, 2), hcas=round(hcas, 2), SL=SL, loseta=loseta, vig=vig, cas=cas, pp=loseta + vig + cas)


def cargas(pid):
    u, l = USO[pid], losa(pid)
    sobre = u["pisos"][1] + u["cielo"][1] + u["ductos"] + u["muros"][1]
    cub_sobre = AFINADO_CUB[1] + u["imper"][1] + (u["terraza"][1] if u["terraza"] else 0) + u["cielo"][1] + u["ductos"]
    return dict(losa_pp=round(l["pp"], 2), D_ent=round(l["pp"] + sobre, 2), D_ent_sobre=round(sobre, 2),
                D_cub=round(l["pp"] + cub_sobre, 2), D_cub_sobre=round(cub_sobre, 2), L=u["L"][1], Lc=u["Lc"][1], h_losa=l["h"])


def edificios():
    out = []
    for pid, sx, sy, desc in PLANTAS:
        u = USO[pid]
        for n in PISOS[pid]:
            out.append(dict(id=f"{pid}-{n}P", planta=pid, sx=sx, sy=sy, pisos=n, desc=desc,
                            uso=u["uso"], grupo=u["grupo"], I=u["I"], **cargas(pid)))
    return out


if __name__ == "__main__":
    for pid, *_ in PLANTAS:
        print(pid, losa(pid)["h"], cargas(pid))
