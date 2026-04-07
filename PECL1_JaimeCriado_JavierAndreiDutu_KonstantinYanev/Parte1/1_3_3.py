import subprocess
import re
import csv
import os

DOMINIO = "domain.pddl"
PROBLEMA = "problem_d1_r0_l6_p6_c6_g6.pddl"
N = 6
LIMITE_TIEMPO = 60

CARPETA_RESULTADOS = "resultados_1_3_3"
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CSV_RESULTADOS = os.path.join(CARPETA_RESULTADOS, "resultados_1_3_3.csv")

PRUEBAS = [
    {"nombre": "BFS", "search": "bfs", "heuristica": None, "optimo": "si"},
    {"nombre": "IDS", "search": "ids", "heuristica": None, "optimo": "si"},
    {"nombre": "A*_hMAX", "search": "astar", "heuristica": "hmax", "optimo": "si"},
    {"nombre": "A*_LMCUT", "search": "astar", "heuristica": "lmcut", "optimo": "si"},
]


def ejecutar_pyperplan(problema, prueba):
    comando = ["pyperplan", "-s", prueba["search"]]

    if prueba["heuristica"] is not None:
        comando += ["-H", prueba["heuristica"]]

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


def guardar_csv(resultados):
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

    print("BENCHMARK 1.3.3")
    print("=" * 60)

    if not os.path.exists(DOMINIO):
        print(f"Error: no existe el dominio '{DOMINIO}'.")
        return

    if not os.path.exists(PROBLEMA):
        print(f"Error: no existe el problema '{PROBLEMA}'.")
        return

    print(f"Usando problema fijo: {PROBLEMA}")

    for prueba in PRUEBAS:
        print(f"\nProbando {prueba['nombre']}...")

        resultado = ejecutar_pyperplan(PROBLEMA, prueba)

        fila = {
            "algoritmo": prueba["nombre"],
            "n": N,
            "problema": PROBLEMA,
            "resuelto": resultado["resuelto"],
            "tiempo_segundos": resultado["tiempo_segundos"],
            "longitud_plan": resultado["longitud_plan"],
            "optimo": prueba["optimo"],
            "motivo": resultado["motivo"]
        }
        resultados.append(fila)

        if resultado["resuelto"] == "si":
            print(f"  OK | tiempo = {resultado['tiempo_segundos']} s | plan = {resultado['longitud_plan']}")
        else:
            if resultado["motivo"] == "timeout":
                print("  TIMEOUT")
            else:
                print("  No resuelto")

    guardar_csv(resultados)

    print("\n" + "=" * 60)
    print("Benchmark terminado.")
    print(f"CSV guardado en: {CSV_RESULTADOS}")


if __name__ == "__main__":
    main()