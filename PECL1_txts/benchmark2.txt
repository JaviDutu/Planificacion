import subprocess
import re
import csv
import os

# Cosas fijas del benchmark
DOMINIO = "domain.pddl"
LIMITE_TIEMPO = 60
INICIO = 5
SALTO = 5
MAX_N = 200

# Carpeta donde guardar resultados
CARPETA_RESULTADOS = "resultados_benchmark"
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CSV_SALIDA = os.path.join(CARPETA_RESULTADOS, "resultados.csv")


def nombre_problema(n):
    return f"problem_d1_r0_l{n}_p{n}_c{n}_g{n}.pddl"


def generar_problema(n):
    problema = nombre_problema(n)

    # Si ya existe, lo reutilizamos
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


def ejecutar_ff(fichero_problema):
    comando = ["planutils", "run", "ff", DOMINIO, fichero_problema]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=LIMITE_TIEMPO
        )

        salida = resultado.stdout

        # Si no aparece esto, asumimos que no ha encontrado plan
        if "found legal plan as follows" not in salida:
            return {
                "resuelto": "no",
                "tiempo_segundos": "",
                "longitud_plan": "",
                "motivo": "sin_solucion"
            }

        # Sacar el tiempo total de FF
        tiempo = ""
        match_tiempo = re.search(r"(\d+\.\d+)\s+seconds total time", salida)
        if match_tiempo:
            tiempo = match_tiempo.group(1)

        # Contar pasos del plan
        pasos = len(re.findall(r"^\s*(?:step\s+)?\d+:", salida, re.MULTILINE))

        return {
            "resuelto": "si",
            "tiempo_segundos": tiempo,
            "longitud_plan": pasos,
            "motivo": "ok"
        }

    except subprocess.TimeoutExpired:
        return {
            "resuelto": "no",
            "tiempo_segundos": "",
            "longitud_plan": "",
            "motivo": "timeout"
        }


def guardar_resultados(resultados):
    with open(CSV_SALIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(
            f,
            fieldnames=["n", "problema", "resuelto", "tiempo_segundos", "longitud_plan", "motivo"]
        )
        escritor.writeheader()
        escritor.writerows(resultados)


def probar_tamano(n, resultados):
    problema = nombre_problema(n)

    print("=" * 50)
    print(f"Probando n = {n}")

    try:
        generar_problema(n)
    except subprocess.CalledProcessError:
        print("Error al generar el problema.")
        fila = {
            "n": n,
            "problema": problema,
            "resuelto": "no",
            "tiempo_segundos": "",
            "longitud_plan": "",
            "motivo": "error_generacion"
        }
        resultados.append(fila)
        return fila

    resultado_ff = ejecutar_ff(problema)

    fila = {
        "n": n,
        "problema": problema,
        "resuelto": resultado_ff["resuelto"],
        "tiempo_segundos": resultado_ff["tiempo_segundos"],
        "longitud_plan": resultado_ff["longitud_plan"],
        "motivo": resultado_ff["motivo"]
    }

    resultados.append(fila)

    if resultado_ff["resuelto"] == "si":
        print(f"Resuelto en {resultado_ff['tiempo_segundos']} s | longitud del plan: {resultado_ff['longitud_plan']}")
    else:
        if resultado_ff["motivo"] == "timeout":
            print("FF ha superado 60 segundos.")
        elif resultado_ff["motivo"] == "sin_solucion":
            print("FF no ha encontrado solución.")
        else:
            print("Ha fallado la ejecución.")

    return fila


def refinar_ultimo_tramo(inicio_refinado, fin_refinado, resultados):
    ultimo_resuelto_refinado = None

    print("\n" + "=" * 50)
    print(f"Refinando de 1 en 1 desde n = {inicio_refinado} hasta n = {fin_refinado}")
    print("=" * 50)

    for n in range(inicio_refinado, fin_refinado + 1):
        fila = probar_tamano(n, resultados)

        if fila["resuelto"] == "si":
            ultimo_resuelto_refinado = n

    return ultimo_resuelto_refinado


def main():
    resultados = []
    ultimo_resuelto = None
    timeout_encontrado = False
    n_timeout = None

    print("Barrido de 5 en 5")
    print("=" * 50)

    for n in range(INICIO, MAX_N + 1, SALTO):
        fila = probar_tamano(n, resultados)

        if fila["resuelto"] == "si":
            ultimo_resuelto = n
        else:
            if fila["motivo"] == "timeout":
                timeout_encontrado = True
                n_timeout = n
            break

    # Si el primer fallo fue por timeout, refinamos el último tramo de 5
    if timeout_encontrado and n_timeout is not None:
        if ultimo_resuelto is not None:
            inicio_refinado = ultimo_resuelto + 1
        else:
            inicio_refinado = max(1, n_timeout - SALTO + 1)

        fin_refinado = n_timeout - 1

        if inicio_refinado <= fin_refinado:
            ultimo_refinado = refinar_ultimo_tramo(inicio_refinado, fin_refinado, resultados)
            if ultimo_refinado is not None:
                ultimo_resuelto = ultimo_refinado

    guardar_resultados(resultados)

    print("\n" + "=" * 50)
    print("Benchmark terminado.")
    if ultimo_resuelto is not None:
        print(f"Último tamaño resuelto dentro del límite: n = {ultimo_resuelto}")
    else:
        print("No se ha resuelto ningún problema dentro del límite.")
    print(f"CSV guardado en: {CSV_SALIDA}")


if __name__ == "__main__":
    main()