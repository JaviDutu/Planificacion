import subprocess
import csv
import os
import re
import glob

# =========================================================
# CONFIGURACION
# =========================================================

DOMINIO = "domain.pddl"
GENERADOR = "generate-problem.py"

LIMITE_TIEMPO = 60
INICIO = 5
SALTO = 5
MAX_N = 200

CARPETA_RESULTADOS = "resultados_2_2"
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CSV_DETALLADO = os.path.join(CARPETA_RESULTADOS, "resultados_2_2_detallado.csv")
CSV_RESUMEN = os.path.join(CARPETA_RESULTADOS, "resultados_2_2_resumen.csv")

PLANIFICADORES = [
    {
        "nombre": "metric-ff",
        "tipo": "satisficing",
        "comando": lambda problema: [
            "planutils", "run", "metric-ff", DOMINIO, problema
        ]
    },
    {
        "nombre": "lama-first",
        "tipo": "satisficing",
        "comando": lambda problema: [
            "planutils", "run", "lama-first", "--", DOMINIO, problema
        ]
    },
    {
        "nombre": "seq-sat-fdss-2",
        "tipo": "satisficing",
        "comando": lambda problema: [
            "planutils", "run", "downward", "--",
            "--alias", "seq-sat-fdss-2",
            "--search-time-limit", "60s",
            DOMINIO, problema
        ]
    },
    {
        "nombre": "seq-sat-fd-autotune-2",
        "tipo": "satisficing",
        "comando": lambda problema: [
            "planutils", "run", "downward", "--",
            "--alias", "seq-sat-fd-autotune-2",
            "--search-time-limit", "60s",
            DOMINIO, problema
        ]
    },
    {
        "nombre": "seq-opt-lmcut",
        "tipo": "optimo",
        "comando": lambda problema: [
            "planutils", "run", "downward", "--",
            "--alias", "seq-opt-lmcut",
            DOMINIO, problema
        ]
    },
    {
        "nombre": "seq-opt-bjolp",
        "tipo": "optimo",
        "comando": lambda problema: [
            "planutils", "run", "downward", "--",
            "--alias", "seq-opt-bjolp",
            DOMINIO, problema
        ]
    },
    {
        "nombre": "seq-opt-fdss-2",
        "tipo": "optimo",
        "comando": lambda problema: [
            "planutils", "run", "downward", "--",
            "--alias", "seq-opt-fdss-2",
            "--search-time-limit", "60s",
            DOMINIO, problema
        ]
    },
]

# =========================================================
# UTILIDADES
# =========================================================

def nombre_problema(n):
    return f"problem_d1_r1_l{n}_p{n}_c{n}_g{n}.pddl"


def limpiar_planes():
    for patron in ["sas_plan*", "plan.soln*", "output.sas"]:
        for fichero in glob.glob(patron):
            try:
                os.remove(fichero)
            except OSError:
                pass


def generar_problema(n):
    problema = nombre_problema(n)

    if os.path.exists(problema):
        return problema

    comando = [
        "python3", GENERADOR,
        "-d", "1",
        "-r", "1",
        "-l", str(n),
        "-p", str(n),
        "-c", str(n),
        "-g", str(n)
    ]

    subprocess.run(
        comando,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return problema


def leer_fichero(ruta):
    try:
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def encontrar_mejor_plan():
    candidatos = []
    for patron in ["sas_plan*", "plan.soln*"]:
        candidatos.extend(glob.glob(patron))

    if not candidatos:
        return None

    mejor = None
    mejor_coste = None
    mejor_mtime = None

    for ruta in candidatos:
        texto = leer_fichero(ruta)
        coste_txt = extraer_coste(texto)
        try:
            coste_num = float(coste_txt) if coste_txt != "" else None
        except ValueError:
            coste_num = None

        try:
            mtime = os.path.getmtime(ruta)
        except OSError:
            mtime = 0

        if mejor is None:
            mejor = ruta
            mejor_coste = coste_num
            mejor_mtime = mtime
            continue

        if coste_num is not None and mejor_coste is not None:
            if coste_num < mejor_coste:
                mejor = ruta
                mejor_coste = coste_num
                mejor_mtime = mtime
            elif coste_num == mejor_coste and mtime > mejor_mtime:
                mejor = ruta
                mejor_coste = coste_num
                mejor_mtime = mtime
        elif coste_num is not None and mejor_coste is None:
            mejor = ruta
            mejor_coste = coste_num
            mejor_mtime = mtime
        elif coste_num is None and mejor_coste is None and mtime > mejor_mtime:
            mejor = ruta
            mejor_mtime = mtime

    return mejor


def extraer_tiempo_total(texto):
    patrones = [
        r"([0-9.]+)\s+seconds total time",
        r"Total time:\s*([0-9.]+)s",
        r"Planner time:\s*([0-9.]+)s",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def extraer_tiempo_busqueda(texto):
    patrones = [
        r"Search time:\s*([0-9.]+)s",
        r"Search time:\s*([0-9.]+)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def extraer_coste(texto):
    patrones = [
        r";\s*cost\s*=\s*([0-9]+(?:\.[0-9]+)?)",
        r"Plan cost:\s*([0-9]+(?:\.[0-9]+)?)",
        r"plan cost:\s*([0-9]+(?:\.[0-9]+)?)",
        r"Cost:\s*([0-9]+(?:\.[0-9]+)?)",
        r"cost of plan:\s*([0-9]+(?:\.[0-9]+)?)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def extraer_longitud(texto):
    patrones = [
        r"Plan length:\s*([0-9]+)",
        r"plan length:\s*([0-9]+)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)

    pasos = re.findall(r"^\s*(?:step\s+)?\d+:", texto, re.MULTILINE | re.IGNORECASE)
    if pasos:
        return str(len(pasos))

    return ""


def detectar_solucion(nombre_planificador, salida, plan_file):
    if plan_file is not None:
        return True

    texto = salida.lower()

    if nombre_planificador == "metric-ff":
        return (
            "found legal plan as follows" in texto
            or "found plan" in texto
        )

    return (
        "solution found" in texto
        or "plan length:" in texto
        or "cost of plan:" in texto
        or "search successful" in texto
    )


def ejecutar_planificador(planificador, problema):
    limpiar_planes()

    comando = planificador["comando"](problema)

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=LIMITE_TIEMPO
        )

        salida = (resultado.stdout or "") + "\n" + (resultado.stderr or "")
        plan_file = encontrar_mejor_plan()

        resuelto = detectar_solucion(planificador["nombre"], salida, plan_file)

        tiempo_total = extraer_tiempo_total(salida)
        tiempo_busqueda = extraer_tiempo_busqueda(salida)
        coste = extraer_coste(salida)
        longitud = extraer_longitud(salida)

        if plan_file is not None:
            texto_plan = leer_fichero(plan_file)

            coste_plan = extraer_coste(texto_plan)
            longitud_plan = extraer_longitud(texto_plan)

            if coste == "" and coste_plan != "":
                coste = coste_plan
            if longitud == "" and longitud_plan != "":
                longitud = longitud_plan

        fila = {
            "planificador": planificador["nombre"],
            "tipo": planificador["tipo"],
            "n": extraer_n_desde_problema(problema),
            "problema": problema,
            "resuelto": "si" if resuelto else "no",
            "motivo": "ok" if resuelto else "sin_solucion",
            "tiempo_total_s": tiempo_total,
            "tiempo_busqueda_s": tiempo_busqueda,
            "coste_plan": coste,
            "longitud_plan": longitud,
            "returncode": resultado.returncode,
        }

        limpiar_planes()
        return fila

    except subprocess.TimeoutExpired:
        limpiar_planes()
        return {
            "planificador": planificador["nombre"],
            "tipo": planificador["tipo"],
            "n": extraer_n_desde_problema(problema),
            "problema": problema,
            "resuelto": "no",
            "motivo": "timeout",
            "tiempo_total_s": "",
            "tiempo_busqueda_s": "",
            "coste_plan": "",
            "longitud_plan": "",
            "returncode": "timeout",
        }


def extraer_n_desde_problema(problema):
    m = re.search(r"_l(\d+)_p\d+_c\d+_g\d+\.pddl$", problema)
    if m:
        return int(m.group(1))
    return ""


def probar_n(planificador, n, resultados_detallados):
    problema = nombre_problema(n)

    print(f"  Probando n = {n}")

    try:
        generar_problema(n)
    except subprocess.CalledProcessError:
        fila = {
            "planificador": planificador["nombre"],
            "tipo": planificador["tipo"],
            "n": n,
            "problema": problema,
            "resuelto": "no",
            "motivo": "error_generacion",
            "tiempo_total_s": "",
            "tiempo_busqueda_s": "",
            "coste_plan": "",
            "longitud_plan": "",
            "returncode": "error",
        }
        resultados_detallados.append(fila)
        print("    Error al generar el problema")
        return fila

    fila = ejecutar_planificador(planificador, problema)
    resultados_detallados.append(fila)

    if fila["resuelto"] == "si":
        print(
            f"    OK | tiempo_total = {fila['tiempo_total_s']} s "
            f"| tiempo_busqueda = {fila['tiempo_busqueda_s']} s "
            f"| coste = {fila['coste_plan']} | plan = {fila['longitud_plan']}"
        )
    else:
        print(f"    {fila['motivo'].upper()}")

    return fila


def refinar_tramo(planificador, inicio_refinado, fin_refinado, resultados_detallados):
    ultimo_ok = None

    if inicio_refinado > fin_refinado:
        return None

    print(f"  Refinando de 1 en 1: {inicio_refinado}..{fin_refinado}")

    for n in range(inicio_refinado, fin_refinado + 1):
        fila = probar_n(planificador, n, resultados_detallados)
        if fila["resuelto"] == "si":
            ultimo_ok = fila

    return ultimo_ok


def benchmark_planificador(planificador, resultados_detallados):
    print("\n" + "=" * 70)
    print(f"Planificador: {planificador['nombre']} ({planificador['tipo']})")
    print("=" * 70)

    ultimo_ok = None
    primer_fallo_n = None

    for n in range(INICIO, MAX_N + 1, SALTO):
        fila = probar_n(planificador, n, resultados_detallados)

        if fila["resuelto"] == "si":
            ultimo_ok = fila
        else:
            primer_fallo_n = n
            break

    if primer_fallo_n is not None:
        if ultimo_ok is not None:
            inicio_refinado = ultimo_ok["n"] + 1
        else:
            inicio_refinado = max(1, primer_fallo_n - SALTO + 1)

        fin_refinado = primer_fallo_n - 1

        mejor_refinado = refinar_tramo(
            planificador,
            inicio_refinado,
            fin_refinado,
            resultados_detallados
        )

        if mejor_refinado is not None:
            ultimo_ok = mejor_refinado

    if ultimo_ok is None:
        resumen = {
            "planificador": planificador["nombre"],
            "tipo": planificador["tipo"],
            "max_n_resuelto": "",
            "problema_maximo": "",
            "tiempo_total_s": "",
            "tiempo_busqueda_s": "",
            "coste_plan": "",
            "longitud_plan": "",
            "resultado": "no_resuelve_ninguno",
        }
    else:
        resumen = {
            "planificador": planificador["nombre"],
            "tipo": planificador["tipo"],
            "max_n_resuelto": ultimo_ok["n"],
            "problema_maximo": ultimo_ok["problema"],
            "tiempo_total_s": ultimo_ok["tiempo_total_s"],
            "tiempo_busqueda_s": ultimo_ok["tiempo_busqueda_s"],
            "coste_plan": ultimo_ok["coste_plan"],
            "longitud_plan": ultimo_ok["longitud_plan"],
            "resultado": "ok",
        }

    return resumen


def guardar_csv_detallado(resultados):
    with open(CSV_DETALLADO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "planificador",
                "tipo",
                "n",
                "problema",
                "resuelto",
                "motivo",
                "tiempo_total_s",
                "tiempo_busqueda_s",
                "coste_plan",
                "longitud_plan",
                "returncode",
            ]
        )
        writer.writeheader()
        writer.writerows(resultados)


def guardar_csv_resumen(resumenes):
    with open(CSV_RESUMEN, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "planificador",
                "tipo",
                "max_n_resuelto",
                "problema_maximo",
                "tiempo_total_s",
                "tiempo_busqueda_s",
                "coste_plan",
                "longitud_plan",
                "resultado",
            ]
        )
        writer.writeheader()
        writer.writerows(resumenes)


def main():
    if not os.path.exists(DOMINIO):
        print(f"Error: no existe {DOMINIO}")
        return

    if not os.path.exists(GENERADOR):
        print(f"Error: no existe {GENERADOR}")
        return

    resultados_detallados = []
    resumenes = []

    print("BENCHMARK PARTE 2.2")
    print("Buscando el mayor tamaño resuelto por cada planificador en <= 60 s")

    for planificador in PLANIFICADORES:
        resumen = benchmark_planificador(planificador, resultados_detallados)
        resumenes.append(resumen)

        guardar_csv_detallado(resultados_detallados)
        guardar_csv_resumen(resumenes)

        if resumen["resultado"] == "ok":
            print(
                f"\nResumen {planificador['nombre']}: "
                f"max_n = {resumen['max_n_resuelto']} | "
                f"coste = {resumen['coste_plan']} | "
                f"plan = {resumen['longitud_plan']} | "
                f"tiempo_total = {resumen['tiempo_total_s']} s"
            )
        else:
            print(f"\nResumen {planificador['nombre']}: no resolvió ningún tamaño")

    print("\n" + "=" * 70)
    print("Benchmark terminado.")
    print(f"CSV detallado: {CSV_DETALLADO}")
    print(f"CSV resumen: {CSV_RESUMEN}")


if __name__ == "__main__":
    main()