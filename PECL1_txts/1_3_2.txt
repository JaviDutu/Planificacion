import subprocess
import re
import csv
import os

DOMINIO = "domain.pddl"
PROBLEMA = "problem_d1_r0_l8_p8_c8_g8.pddl"
N = 8
LIMITE_TIEMPO = 60

CARPETA_RESULTADOS = "resultados_1_3_2"
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CSV_RESULTADOS = os.path.join(CARPETA_RESULTADOS, "resultados_1_3_2.csv")

BUSQUEDAS = [
    {"nombre": "GBFS", "search": "gbf"},
    {"nombre": "EHC", "search": "ehs"}
]

HEURISTICAS = [
    {"nombre": "hMAX", "heuristica": "hmax"},
    {"nombre": "hADD", "heuristica": "hadd"},
    {"nombre": "hFF", "heuristica": "hff"},
    {"nombre": "Landmark", "heuristica": "landmark"}
]


def ejecutar_pyperplan(problema, search, heuristica):
    comando = [
        "pyperplan",
        "-s", search,
        "-H", heuristica,
        DOMINIO,
        problema
    ]

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
                "busqueda", "heuristica", "n", "problema",
                "resuelto", "tiempo_segundos", "longitud_plan", "motivo"
            ]
        )
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    resultados = []

    print("BENCHMARK 1.3.2")
    print("=" * 60)

    if not os.path.exists(DOMINIO):
        print(f"Error: no existe el dominio '{DOMINIO}'.")
        return

    if not os.path.exists(PROBLEMA):
        print(f"Error: no existe el problema '{PROBLEMA}'.")
        return

    print(f"Usando problema fijo: {PROBLEMA}")

    for busqueda in BUSQUEDAS:
        for heuristica in HEURISTICAS:
            print(f"\nProbando {busqueda['nombre']} + {heuristica['nombre']}...")

            resultado = ejecutar_pyperplan(
                PROBLEMA,
                busqueda["search"],
                heuristica["heuristica"]
            )

            fila = {
                "busqueda": busqueda["nombre"],
                "heuristica": heuristica["nombre"],
                "n": N,
                "problema": PROBLEMA,
                "resuelto": resultado["resuelto"],
                "tiempo_segundos": resultado["tiempo_segundos"],
                "longitud_plan": resultado["longitud_plan"],
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