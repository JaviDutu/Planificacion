import csv
import os
import matplotlib.pyplot as plt

CSV_ENTRADA = "resultados_benchmark/resultados.csv"
CARPETA_SALIDA = "resultados_benchmark"
IMAGEN_SALIDA = os.path.join(CARPETA_SALIDA, "grafica_tiempo.png")


def leer_resultados():
    tamanos = []
    tiempos = []

    with open(CSV_ENTRADA, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)

        for fila in lector:
            if fila["resuelto"] == "si" and fila["tiempo_segundos"] != "":
                tamanos.append(int(fila["n"]))
                tiempos.append(float(fila["tiempo_segundos"]))

    return tamanos, tiempos


def main():
    tamanos, tiempos = leer_resultados()

    if not tamanos:
        print("No hay datos resueltos para representar.")
        return

    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, tiempos, marker="o")
    plt.xlabel("Tamaño del problema (n)")
    plt.ylabel("Tiempo de resolución (s)")
    plt.title("Tiempo de resolución de FF según el tamaño del problema")
    plt.grid(True)

    plt.savefig(IMAGEN_SALIDA, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Gráfica guardada en: {IMAGEN_SALIDA}")


if __name__ == "__main__":
    main()