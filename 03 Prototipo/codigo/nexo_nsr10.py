"""
Nexo Sísmico · Módulo NSR-10 (prototipo B)
Análisis sísmico preliminar de pórticos de concreto según NSR-10 (Títulos A y B),
con validación de entradas, FHE, derivas con 12 combinaciones en esquinas, índice de
estabilidad Q y coeficiente R. Caso de calibración: proyecto del curso, grupo 1
(oficinas, 5 pisos, Bogotá, microzona Piedemonte A).

Uso:
    from nexo_nsr10 import analizar
    resultado = analizar(datos_json)      # dict con "estado": "ok" | "faltan_datos" | "datos_invalidos"
"""
import math, json

VERSION = "1.0 (2026-10-24)"

# --------------------------------------------------------------------------- #
# 1. ESQUEMA DE ENTRADA Y VALIDACIÓN                                           #
# --------------------------------------------------------------------------- #
COMBOS = [f"DER-X{i}" for i in range(1, 7)] + [f"DER-Y{i}" for i in range(1, 7)]
# DER-X1 +FX · X2 +FX+MZFX · X3 +FX−MZFX · X4 −FX · X5 −FX+MZFX · X6 −FX−MZFX (igual en Y)

CAMPOS = {   # ruta: (tipo, mínimo, máximo, descripción, unidad)
    "sitio.Aa":               (float, 0.05, 0.50, "coeficiente de aceleración Aa", "-"),
    "sitio.Av":               (float, 0.05, 0.50, "coeficiente de velocidad Av", "-"),
    "sitio.Fa":               (float, 0.80, 3.00, "coeficiente de amplificación Fa", "-"),
    "sitio.Fv":               (float, 0.80, 4.00, "coeficiente de amplificación Fv", "-"),
    "sitio.TL":               (float, 1.00, 10.0, "periodo largo TL", "s"),
    "sitio.grupo_uso":        (int,   1,    4,    "grupo de uso (A.2.5)", "-"),
    "sistema.R0":             (float, 2.5,  8.0,  "coeficiente básico de disipación R0", "-"),
    "geometria.Bx":           (float, 3.0,  200., "dimensión total de la planta en X", "m"),
    "geometria.By":           (float, 3.0,  200., "dimensión total de la planta en Y", "m"),
    "geometria.h_losa":       (float, 0.10, 1.20, "espesor de losa", "m"),
    "periodos_sap.Tx":        (float, 0.05, 5.0,  "periodo fundamental en X de SAP2000", "s"),
    "periodos_sap.Ty":        (float, 0.05, 5.0,  "periodo fundamental en Y de SAP2000", "s"),
}
LISTAS = {   # ruta: (mínimo, máximo, descripción, unidad)
    "geometria.alturas_libres": (1.8, 6.0,  "altura libre de entrepiso", "m"),
    "pesos.W_kN":               (1.0, 1e6,  "peso sísmico por nivel W", "kN"),
    "pesos.L_kN":               (0.0, 1e6,  "carga viva por nivel L", "kN"),
}


def _get(d, ruta):
    for k in ruta.split("."):
        if not isinstance(d, dict) or k not in d or d[k] in (None, ""):
            return None
        d = d[k]
    return d


def validar(datos):
    """Devuelve (estado, faltantes, errores, advertencias)."""
    faltan, errores, avisos = [], [], []
    for ruta, (tipo, lo, hi, desc, un) in CAMPOS.items():
        v = _get(datos, ruta)
        if v is None:
            faltan.append(f"{ruta} — {desc} [{un}]")
            continue
        try:
            v = tipo(v)
        except (TypeError, ValueError):
            errores.append(f"{ruta} = {v!r}: debe ser numérico ({desc})")
            continue
        if not (lo <= v <= hi):
            errores.append(f"{ruta} = {v} {un}: fuera del rango válido [{lo}, {hi}] {un} ({desc})")
    n = None
    for ruta, (lo, hi, desc, un) in LISTAS.items():
        v = _get(datos, ruta)
        if v is None:
            faltan.append(f"{ruta} — {desc} por nivel [{un}]")
            continue
        if not isinstance(v, list) or not v:
            errores.append(f"{ruta}: debe ser una lista con un valor por nivel")
            continue
        n = n or len(v)
        if len(v) != n:
            errores.append(f"{ruta}: tiene {len(v)} valores y se esperaban {n} (uno por nivel)")
        for i, x in enumerate(v, 1):
            if not isinstance(x, (int, float)):
                errores.append(f"{ruta}[nivel {i}] = {x!r}: debe ser numérico")
            elif not (lo <= x <= hi):
                pista = " — ¿está en centímetros en lugar de metros?" if un == "m" and x > 10 * hi / 6 else ""
                errores.append(f"{ruta}[nivel {i}] = {x} {un}: fuera del rango válido [{lo}, {hi}] {un}{pista}")
    # Derivas: 12 combinaciones en dos esquinas opuestas, un valor por nivel
    esq = _get(datos, "derivas_sap.esquinas")
    if esq is None:
        faltan.append("derivas_sap.esquinas — desplazamientos U1, U2 de SAP2000 en dos esquinas (12 combinaciones)")
    else:
        if len(esq) < 2:
            errores.append("derivas_sap.esquinas: se requieren dos esquinas opuestas de la planta")
        for nom, e in esq.items():
            for c in COMBOS:
                filas = (e.get("combinaciones") or {}).get(c)
                if filas is None:
                    faltan.append(f"derivas_sap.esquinas.{nom}.combinaciones.{c}")
                elif n and len(filas) != n:
                    errores.append(f"esquina {nom}, {c}: {len(filas)} niveles y se esperaban {n}")
    # Coherencia física (solo si lo básico existe)
    Aa, Fa = _get(datos, "sitio.Aa"), _get(datos, "sitio.Fa")
    if isinstance(Aa, (int, float)) and isinstance(Fa, (int, float)) and Aa > 0.2 and _get(datos, "sistema.R0") == 2.5:
        avisos.append("R0 = 2.5 (DMI) no se permite en amenaza intermedia/alta (A.3.1)")
    estado = "faltan_datos" if faltan else ("datos_invalidos" if errores else "ok")
    return estado, faltan, errores, avisos


# --------------------------------------------------------------------------- #
# 2. CÁLCULO NSR-10                                                            #
# --------------------------------------------------------------------------- #
I_GRUPO = {1: 1.00, 2: 1.10, 3: 1.25, 4: 1.50}                 # Tabla A.2.5-1


def espectro(T, Aa, Av, Fa, Fv, I, TL):
    """Sa (g) de la Figura A.2.6-1 para el modo fundamental (meseta desde T = 0)."""
    Tc = 0.48 * Av * Fv / (Aa * Fa)
    if T <= Tc:
        return 2.5 * Aa * Fa * I, "meseta"
    if T <= TL:
        return 1.2 * Av * Fv * I / T, "descendente 1/T"
    return 1.2 * Av * Fv * TL * I / T ** 2, "largo periodo 1/T²"


def analizar(datos):
    estado, faltan, errores, avisos = validar(datos)
    out = {"version": VERSION, "estado": estado, "faltan": faltan, "errores": errores, "advertencias": avisos}
    if estado != "ok":
        out["mensaje"] = ("No se puede calcular: faltan datos." if estado == "faltan_datos"
                          else "No se puede calcular: hay datos fuera de rango o inconsistentes.")
        return out

    s, g, p = datos["sitio"], datos["geometria"], datos["pesos"]
    Aa, Av, Fa, Fv, TL = (float(s[k]) for k in ("Aa", "Av", "Fa", "Fv", "TL"))
    I = I_GRUPO[int(s["grupo_uso"])]
    hl, hlosa = g["alturas_libres"], float(g["h_losa"])
    hpi = [x + hlosa for x in hl]                               # altura de piso (eje a eje de losa)
    Z = [sum(hpi[:i + 1]) for i in range(len(hpi))]
    hn, n = Z[-1], len(hpi)
    W, L = p["W_kN"], p["L_kN"]
    Wt = sum(W)

    # A.4.2 periodo
    Ta = 0.047 * hn ** 0.90
    Cu = max(1.20, 1.75 - 1.20 * Av * Fv)
    CuTa = Cu * Ta
    T_sap = {"X": float(datos["periodos_sap"]["Tx"]), "Y": float(datos["periodos_sap"]["Ty"])}
    T_dis = {d: min(T, CuTa) for d, T in T_sap.items()}
    for d in "XY":
        if T_sap[d] > CuTa:
            avisos.append(f"T{d.lower()} de SAP ({T_sap[d]:.3f} s) > Cu·Ta ({CuTa:.3f} s): se usa Cu·Ta (A.4.2.1)")

    # A.4.3 cortante y distribución
    fhe = {}
    for d in "XY":
        Sa, tramo = espectro(T_dis[d], Aa, Av, Fa, Fv, I, TL)
        Vs = Sa * Wt
        T = T_dis[d]
        k = 1.0 if T <= 0.5 else (2.0 if T >= 2.5 else 0.75 + 0.5 * T)
        mh = [W[i] * Z[i] ** k for i in range(n)]
        F = [Vs * x / sum(mh) for x in mh]
        V = [sum(F[i:]) for i in range(n)]
        e = 0.05 * (float(g["By"]) if d == "X" else float(g["Bx"]))   # A.3.6.7.1
        fhe[d] = {"T_sap": T_sap[d], "T_diseno": T, "Sa": Sa, "tramo": tramo, "Vs": Vs, "k": k,
                  "F": F, "V": V, "e_acc": e, "Mz": [f * e for f in F]}

    # A.6 derivas: Δ = √(Δx² + Δy²) por piso, en cada esquina y combinación
    lim = float(datos.get("limite_deriva", 0.010))
    der = {"X": [0.0] * n, "Y": [0.0] * n}
    der_combo = {"X": [""] * n, "Y": [""] * n}
    comp = {}                     # componente en la dirección del sismo, por esquina y combinación (torsión)
    for nom, e in datos["derivas_sap"]["esquinas"].items():
        for c in COMBOS:
            d = c[4]
            U = e["combinaciones"][c]
            prev = (0.0, 0.0)
            for i, (u1, u2) in enumerate(U):
                dx, dy = u1 - prev[0], u2 - prev[1]
                D = math.hypot(dx, dy)
                if D > der[d][i]:
                    der[d][i], der_combo[d][i] = D, f"{c} @ {nom}"
                comp[(nom, c, i)] = abs(dx if d == "X" else dy)
                prev = (u1, u2)
    tabla_der = []
    for d in "XY":
        for i in range(n):
            tabla_der.append({"dir": d, "nivel": i + 1, "hpi_m": hpi[i], "deriva_m": der[d][i],
                              "deriva_pct": 100 * der[d][i] / hpi[i], "combinacion": der_combo[d][i],
                              "cumple": der[d][i] <= lim * hpi[i]})

    # A.6.2.3 índice de estabilidad Q (P = W + L acumulado; V sin R; Δ envolvente de esquina)
    Q = {}
    for d in "XY":
        Q[d] = []
        for i in range(n):
            P = sum(W[i:]) + sum(L[i:])
            q = P * der[d][i] / (fhe[d]["V"][i] * hpi[i])
            Q[d].append(q)
    Qmax = max(max(Q["X"]), max(Q["Y"]))

    # A.3.3 torsión (1aP / 1bP) con las dos esquinas, y R
    esquinas = list(datos["derivas_sap"]["esquinas"])
    ratio_tor = 1.0
    for c in COMBOS:                  # misma combinación, esquinas opuestas (Tabla A.3-6, 1aP/1bP)
        for i in range(n):
            a, b = comp[(esquinas[0], c, i)], comp[(esquinas[1], c, i)]
            if a + b > 0:
                ratio_tor = max(ratio_tor, max(a, b) / ((a + b) / 2))
    phi_p = 0.8 if ratio_tor > 1.4 else (0.9 if ratio_tor > 1.2 else 1.0)
    ret = g.get("retroceso")          # {"A","B","C","D"}: proyección / dimensión en cada dirección
    if ret and ret["A"] / ret["B"] > 0.15 and ret["C"] / ret["D"] > 0.15:
        phi_p = min(phi_p, 0.9)
    phi_a = float(datos.get("sistema", {}).get("phi_a", 1.0))
    phi_r = float(datos.get("sistema", {}).get("phi_r", 1.0))
    R = phi_a * phi_p * phi_r * float(datos["sistema"]["R0"])

    cumple_der = all(r["cumple"] for r in tabla_der)
    out.update({
        "mensaje": "Cálculo completo.",
        "parametros": {"I": I, "Tc": 0.48 * Av * Fv / (Aa * Fa), "TL": TL, "hn": hn, "Wt": Wt,
                       "Ta": Ta, "Cu": Cu, "CuTa": CuTa},
        "niveles": [{"nivel": i + 1, "hpi": hpi[i], "Z": Z[i], "W": W[i], "L": L[i]} for i in range(n)],
        "fhe": fhe, "derivas": tabla_der, "Q": Q, "Q_max": Qmax,
        "torsion_ratio": ratio_tor, "phi_p": phi_p, "phi_a": phi_a, "phi_r": phi_r, "R": R,
        "deriva_max_pct": {d: max(100 * der[d][i] / hpi[i] for i in range(n)) for d in "XY"},
        "dictamen": {"derivas": cumple_der, "estabilidad": Qmax <= 0.30,
                     "p_delta_requerido": Qmax > 0.10},
    })
    return out


# --------------------------------------------------------------------------- #
# 3. REPORTE Y REGISTRO PARA LA BASE DE DATOS                                  #
# --------------------------------------------------------------------------- #
def reporte(r, titulo=""):
    L = [f"=== {titulo} ===", f"Estado: {r['estado'].upper()} — {r['mensaje']}"]
    if r["estado"] != "ok":
        for x in r["faltan"]:
            L.append(f"  ✗ FALTA: {x}")
        for x in r["errores"]:
            L.append(f"  ✗ ERROR: {x}")
        L.append("  → Corrija la entrada y vuelva a ejecutar. No se generó ningún resultado.")
        return "\n".join(L)
    p = r["parametros"]
    L.append(f"hn = {p['hn']:.2f} m · Wt = {p['Wt']:,.0f} kN · I = {p['I']} · Tc = {p['Tc']:.3f} s · TL = {p['TL']} s")
    L.append(f"Ta = {p['Ta']:.4f} s · Cu = {p['Cu']:.3f} · Cu·Ta = {p['CuTa']:.4f} s")
    for d in "XY":
        f = r["fhe"][d]
        L.append(f"Dir {d}: T = {f['T_diseno']:.4f} s · Sa = {f['Sa']:.4f} g ({f['tramo']}) · k = {f['k']:.3f} · "
                 f"Vs = {f['Vs']:,.0f} kN · e acc = {f['e_acc']:.3f} m")
    L.append("Nivel |  Z (m) |   W (kN) |  Fx (kN) |  Fy (kN) | MzFx (kN·m) | MzFy (kN·m)")
    for i, nv in reversed(list(enumerate(r["niveles"]))):
        L.append(f"{nv['nivel']:5d} | {nv['Z']:6.2f} | {nv['W']:8.0f} | {r['fhe']['X']['F'][i]:8.0f} | "
                 f"{r['fhe']['Y']['F'][i]:8.0f} | {r['fhe']['X']['Mz'][i]:11.0f} | {r['fhe']['Y']['Mz'][i]:11.0f}")
    L.append("Derivas (envolvente de 12 combinaciones en las dos esquinas, límite 1.0 % hpi):")
    for x in r["derivas"]:
        L.append(f"  {x['dir']} nivel {x['nivel']}: {x['deriva_pct']:.3f} % ({x['combinacion']}) "
                 f"{'✓' if x['cumple'] else '✗ NO CUMPLE'}")
    L.append(f"Q máx = {r['Q_max']:.4f} → {'P-Delta no requerido' if not r['dictamen']['p_delta_requerido'] else 'considerar P-Delta'}")
    L.append(f"Torsión Δmax/Δprom = {r['torsion_ratio']:.3f} → φp = {r['phi_p']} · R = {r['R']:.2f}")
    L.append(f"DICTAMEN: derivas {'CUMPLEN' if r['dictamen']['derivas'] else 'NO CUMPLEN'} · "
             f"deriva máx X = {r['deriva_max_pct']['X']:.3f} %, Y = {r['deriva_max_pct']['Y']:.3f} %")
    for a in r["advertencias"]:
        L.append(f"  ⚠ {a}")
    return "\n".join(L)


def registro_bd(datos, r):
    """Una fila para la base de datos NSR-10 (mismo esquema que los edificios del profesor)."""
    g = datos["geometria"]
    return {
        "id": datos.get("id", "SIN_ID"), "fuente": datos.get("fuente", ""), "norma": "NSR-10",
        "programa": "SAP2000 + Nexo NSR-10", "estado_dato": datos.get("estado_dato", "verificado"),
        "n_pisos": len(g["alturas_libres"]), "hn_m": r["parametros"]["hn"],
        "Lx_m": g["Bx"], "Ly_m": g["By"], "luces_x_m": g.get("luces_x"), "luces_y_m": g.get("luces_y"),
        "Aa": datos["sitio"]["Aa"], "Av": datos["sitio"]["Av"], "Fa": datos["sitio"]["Fa"], "Fv": datos["sitio"]["Fv"],
        "I": r["parametros"]["I"], "R": r["R"], "W_total_kN": r["parametros"]["Wt"],
        "Tx_s": r["fhe"]["X"]["T_sap"], "Ty_s": r["fhe"]["Y"]["T_sap"], "CuTa_s": r["parametros"]["CuTa"],
        "Sa_x_g": r["fhe"]["X"]["Sa"], "Sa_y_g": r["fhe"]["Y"]["Sa"],
        "Vx_kN": r["fhe"]["X"]["Vs"], "Vy_kN": r["fhe"]["Y"]["Vs"],
        "dx_pct": r["deriva_max_pct"]["X"], "dy_pct": r["deriva_max_pct"]["Y"],
        "columnas": g.get("columnas"),
    }
