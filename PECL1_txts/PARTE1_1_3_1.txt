import subprocess
import re
import csv
import os

DOMINIO = "domain.pddl"
LIMITE_TIEMPO = 60
INICIO = 2
SALTO = 1
MAX_N = 50

# Número de fallos consecutivos permitidos antes de dejar de probar un algoritmo
MAX_FALLOS_CONSECUTIVOS = 2

CARPETA_RESULTADOS = "resultados_1_3_1"
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CSV_RESULTADOS = os.path.join(CARPETA_RESULTADOS, "resultados_1_3_1.csv")

ALGORITMOS = [
    {"nombre": "BFS", "search": "bfs", "heuristica": None, "optimo": "si"},
    {"nombre": "IDS", "search": "ids", "heuristica": None, "optimo": "si"},
    {"nombre": "A*_hMAX", "search": "astar", "heuristica": "hmax", "optimo": "si"},
    {"nombre": "GBFS_hMAX", "search": "gbf", "heuristica": "hmax", "optimo": "no_garantizado"},
]


def nombre_problema(n):
    return f"problem_d1_r0_l{n}_p{n}_c{n}_g{n}.pddl"


def generar_problema_si_no_existe(n):
    problema = nombre_problema(n)

    # Si ya existe, se reutiliza para que la secuencia sea estable entre ejecuciones
    if os.path.exists(problema):
        return problema

    comando = [
        "python3", "generate-problem2.py",
        "-d", "1",
        "-r", "0",
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


def ejecutar_pyperplan(problema, algoritmo):
    comando = ["pyperplan", "-s", algoritmo["search"]]

    if algoritmo["heuristica"] is not None:
        comando += ["-H", algoritmo["heuristica"]]

    comando += [DOMINIO, problema]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=LIMITE_TIEMPO
        )

        salida = resultado.stdout + "\n" + resultado.stderr

        if "Goal reached" not in salida:
            return {
                "resuelto": "no",
                "tiempo_segundos": "",
                "longitud_plan": "",
                "motivo": "sin_solucion"
            }

        tiempo = ""
        match_tiempo = re.search(r"Search time:\s*([0-9.]+)", salida)
        if match_tiempo:
            tiempo = match_tiempo.group(1)

        longitud = ""
        match_longitud = re.search(r"Plan length:\s*(\d+)", salida)
        if match_longitud:
            longitud = match_longitud.group(1)

        return {
            "resuelto": "si",
            "tiempo_segundos": tiempo,
            "longitud_plan": longitud,
            "motivo": "ok"
        }

    except subprocess.TimeoutExpired:
        return {
            "resuelto": "no",
            "tiempo_segundos": "",
            "longitud_plan": "",
            "motivo": "timeout"
        }


def guardar_csv_resultados(resultados):
    with open(CSV_RESULTADOS, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(
            f,
            fieldnames=[
                "algoritmo", "n", "problema", "resuelto",
                "tiempo_segundos", "longitud_plan", "optimo", "motivo"
            ]
        )
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    resultados = []

    ultimo_ok = {}
    activo = {}
    fallos_consecutivos = {}

    for algoritmo in ALGORITMOS:
        nombre = algoritmo["nombre"]
        ultimo_ok[nombre] = None
        activo[nombre] = True
        fallos_consecutivos[nombre] = 0

    print("BENCHMARK 1.3.1")
    print("=" * 60)

    for n in range(INICIO, MAX_N + 1, SALTO):
        if not any(activo.values()):
            print("\nTodos los algoritmos han dejado de resolver dentro del límite.")
            break

        print(f"\nPreparando problema n = {n}")
        try:
            problema = generar_problema_si_no_existe(n)
        except subprocess.CalledProcessError:
            print("Error al generar el problema.")
            break

        for algoritmo in ALGORITMOS:
            nombre = algoritmo["nombre"]

            if not activo[nombre]:
                continue

            print(f"  Probando {nombre}...")

            resultado = ejecutar_pyperplan(problema, algoritmo)

            fila = {
                "algoritmo": nombre,
                "n": n,
                "problema": problema,
                "resuelto": resultado["resuelto"],
                "tiempo_segundos": resultado["tiempo_segundos"],
                "longitud_plan": resultado["longitud_plan"],
                "optimo": algoritmo["optimo"],
                "motivo": resultado["motivo"]
            }
            resultados.append(fila)

            if resultado["resuelto"] == "si":
                print(f"    OK | tiempo = {resultado['tiempo_segundos']} s | plan = {resultado['longitud_plan']}")
                ultimo_ok[nombre] = fila
                fallos_consecutivos[nombre] = 0
            else:
                fallos_consecutivos[nombre] += 1

                if resultado["motivo"] == "timeout":
                    print(f"    TIMEOUT ({fallos_consecutivos[nombre]}/{MAX_FALLOS_CONSECUTIVOS})")
                else:
                    print(f"    No resuelto ({fallos_consecutivos[nombre]}/{MAX_FALLOS_CONSECUTIVOS})")

                if fallos_consecutivos[nombre] >= MAX_FALLOS_CONSECUTIVOS:
                    activo[nombre] = False
                    print(f"    -> {nombre} deja de probarse tras {MAX_FALLOS_CONSECUTIVOS} fallos consecutivos")

    guardar_csv_resultados(resultados)

    print("\n" + "=" * 60)
    print("Resumen final:")
    for algoritmo in ALGORITMOS:
        nombre = algoritmo["nombre"]
        dato = ultimo_ok[nombre]

        if dato is not None:
            print(f"{nombre}: n = {dato['n']} | tiempo = {dato['tiempo_segundos']} s | plan = {dato['longitud_plan']}")
        else:
            print(f"{nombre}: no resolvió ningún tamaño")

    print(f"\nCSV detallado: {CSV_RESULTADOS}")


if __name__ == "__main__":
    main()