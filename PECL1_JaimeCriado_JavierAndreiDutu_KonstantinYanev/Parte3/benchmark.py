#!/usr/bin/env python3

import argparse
import csv
import os
import re
import shutil
import signal
import subprocess
from typing import Dict, List, Optional, Tuple

# =========================================================
# CONFIGURACION
# =========================================================

DOMINIO = "domain.pddl"
GENERADOR = "generate-problem.py"

LIMITE_TIEMPO = 60
INICIO_N = 2
MAX_N = 200

SALTO_GRUESO = 10
RETROCESO_INTERMEDIO = 5

CONFIGURACIONES = [(k, k) for k in range(1, 6)]

REGENERAR_PROBLEMAS = False

CARPETA_RESULTADOS = "resultados_3"
CSV_DETALLADO = os.path.join(CARPETA_RESULTADOS, "resultados_3_detallado.csv")
CSV_RESUMEN = os.path.join(CARPETA_RESULTADOS, "resultados_3_resumen.csv")

os.makedirs(CARPETA_RESULTADOS, exist_ok=True)


# =========================================================
# ARGUMENTOS
# =========================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark definitivo Parte 3 con OPTIC"
    )

    parser.add_argument("--drones", type=int, help="Numero de drones")
    parser.add_argument("--carriers", type=int, help="Numero de transportadores")
    parser.add_argument("--max-n", type=int, default=MAX_N, help="Maximo n a probar")
    parser.add_argument("--regen", action="store_true", help="Regenerar siempre los problemas")
    parser.add_argument(
        "--reset-config",
        action="store_true",
        help="Borrar del CSV y de logs la configuracion indicada con --drones/--carriers antes de ejecutar"
    )

    return parser.parse_args()


# =========================================================
# RUTAS
# =========================================================


def carpeta_logs_config(drones: int, carriers: int) -> str:
    ruta = os.path.join(CARPETA_RESULTADOS, f"logs_d{drones}_r{carriers}")
    os.makedirs(ruta, exist_ok=True)
    return ruta



def ruta_log(drones: int, carriers: int, n: int) -> str:
    return os.path.join(
        carpeta_logs_config(drones, carriers),
        f"optic_d{drones}_r{carriers}_n{n}.log"
    )


# =========================================================
# CSV
# =========================================================

CAMPOS_DETALLADO = [
    "drones",
    "transportadores",
    "n",
    "problema",
    "motivo_final",
    "returncode",
    "num_soluciones",
    "tiempo_primera_solucion_s",
    "duracion_primera_solucion",
    "pasos_primera_solucion",
    "tiempo_ultima_solucion_s",
    "duracion_ultima_solucion",
    "pasos_ultima_solucion",
    "mejora_duracion",
    "mejora_pasos",
    "timeout_s",
    "log",
]

CAMPOS_RESUMEN = [
    "drones",
    "transportadores",
    "max_n_sin_timeout",
    "problema_max_sin_timeout",
    "max_n_con_alguna_solucion",
    "problema_max_con_alguna_solucion",
    "timeout_o_fallo_en_n",
    "motivo_ultimo_intento",
]



def cargar_csv_detallado() -> List[Dict[str, str]]:
    if not os.path.exists(CSV_DETALLADO):
        return []

    with open(CSV_DETALLADO, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))



def cargar_csv_resumen() -> List[Dict[str, str]]:
    if not os.path.exists(CSV_RESUMEN):
        return []

    with open(CSV_RESUMEN, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))



def guardar_csv_detallado(filas: List[Dict[str, object]]) -> None:
    filas_ordenadas = sorted(
        filas,
        key=lambda r: (int(r["drones"]), int(r["transportadores"]), int(r["n"]))
    )

    with open(CSV_DETALLADO, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_DETALLADO)
        writer.writeheader()
        writer.writerows(filas_ordenadas)



def guardar_csv_resumen(filas: List[Dict[str, object]]) -> None:
    filas_ordenadas = sorted(
        filas,
        key=lambda r: (int(r["drones"]), int(r["transportadores"]))
    )

    with open(CSV_RESUMEN, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_RESUMEN)
        writer.writeheader()
        writer.writerows(filas_ordenadas)


# =========================================================
# UTILIDADES
# =========================================================


def nombre_problema(drones: int, carriers: int, n: int) -> str:
    return f"problem_d{drones}_r{carriers}_l{n}_p{n}_c{n}_g{n}.pddl"



def leer_fichero(ruta: str) -> str:
    try:
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""



def generar_problema(drones: int, carriers: int, n: int, regenerar: bool) -> str:
    problema = nombre_problema(drones, carriers, n)

    if regenerar and os.path.exists(problema):
        os.remove(problema)

    if os.path.exists(problema):
        return problema

    comando = [
        "python3", GENERADOR,
        "-d", str(drones),
        "-r", str(carriers),
        "-l", str(n),
        "-p", str(n),
        "-c", str(n),
        "-g", str(n),
    ]

    subprocess.run(
        comando,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return problema



def parsear_planes_optic(texto: str) -> List[Dict[str, object]]:
    """
    Extrae todas las soluciones anytime de OPTIC.

    Cada plan incluye:
    - tiempo_encontrada_s
    - duracion_plan
    - pasos_plan
    - acciones
    """
    planes = []
    actual = None

    re_metric = re.compile(r'^\s*;\s*Plan found with metric\s+([0-9]+(?:\.[0-9]+)?)')
    re_time = re.compile(r'^\s*;\s*Time\s+([0-9]+(?:\.[0-9]+)?)')
    re_accion = re.compile(
        r'^\s*[0-9]+(?:\.[0-9]+)?:\s*\(.*\)\s*\[[0-9]+(?:\.[0-9]+)?\]\s*$'
    )

    def cerrar_actual():
        if actual is not None:
            actual["pasos_plan"] = len(actual["acciones"])
            planes.append(actual)

    for linea in texto.splitlines():
        m_metric = re_metric.match(linea)
        if m_metric:
            cerrar_actual()
            actual = {
                "duracion_plan": float(m_metric.group(1)),
                "tiempo_encontrada_s": None,
                "acciones": []
            }
            continue

        if actual is None:
            continue

        m_time = re_time.match(linea)
        if m_time:
            actual["tiempo_encontrada_s"] = float(m_time.group(1))
            continue

        if re_accion.match(linea):
            actual["acciones"].append(linea.strip())

    cerrar_actual()
    return planes



def ejecutar_optic(problema: str, drones: int, carriers: int, n: int) -> Dict[str, object]:
    """
    Ejecuta OPTIC durante 60 s reales, guardando stdout/stderr en un log.
    """
    log_path = ruta_log(drones, carriers, n)

    comando = [
        "stdbuf", "-oL", "-eL",
        "planutils", "run", "optic",
        DOMINIO, problema
    ]

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    timed_out = False
    returncode = None

    with open(log_path, "w", encoding="utf-8", errors="ignore") as log_file:
        proceso = subprocess.Popen(
            comando,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            start_new_session=True
        )

        try:
            proceso.wait(timeout=LIMITE_TIEMPO)
            returncode = proceso.returncode
        except subprocess.TimeoutExpired:
            timed_out = True

            try:
                os.killpg(proceso.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

            try:
                proceso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proceso.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    proceso.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass

            returncode = "timeout"

    salida = leer_fichero(log_path)
    planes = parsear_planes_optic(salida)

    if timed_out and len(planes) > 0:
        motivo_final = "timeout_con_solucion"
    elif timed_out:
        motivo_final = "timeout_sin_solucion"
    elif len(planes) > 0:
        motivo_final = "ok"
    elif returncode == 0:
        motivo_final = "sin_solucion"
    else:
        motivo_final = "error"

    return {
        "returncode": returncode,
        "motivo_final": motivo_final,
        "num_soluciones": len(planes),
        "planes": planes,
        "log": log_path,
    }


# =========================================================
# CONSTRUCCION DE FILAS
# =========================================================


def construir_fila_detallada(
    drones: int,
    carriers: int,
    n: int,
    problema: str,
    ejecucion: Dict[str, object]
) -> Dict[str, object]:
    planes = ejecucion["planes"]

    if len(planes) == 0:
        return {
            "drones": drones,
            "transportadores": carriers,
            "n": n,
            "problema": problema,
            "motivo_final": ejecucion["motivo_final"],
            "returncode": ejecucion["returncode"],
            "num_soluciones": 0,
            "tiempo_primera_solucion_s": "",
            "duracion_primera_solucion": "",
            "pasos_primera_solucion": "",
            "tiempo_ultima_solucion_s": "",
            "duracion_ultima_solucion": "",
            "pasos_ultima_solucion": "",
            "mejora_duracion": "",
            "mejora_pasos": "",
            "timeout_s": LIMITE_TIEMPO,
            "log": ejecucion["log"],
        }

    primera = planes[0]
    ultima = planes[-1]

    return {
        "drones": drones,
        "transportadores": carriers,
        "n": n,
        "problema": problema,
        "motivo_final": ejecucion["motivo_final"],
        "returncode": ejecucion["returncode"],
        "num_soluciones": len(planes),
        "tiempo_primera_solucion_s": (
            primera["tiempo_encontrada_s"] if primera["tiempo_encontrada_s"] is not None else ""
        ),
        "duracion_primera_solucion": primera["duracion_plan"],
        "pasos_primera_solucion": primera["pasos_plan"],
        "tiempo_ultima_solucion_s": (
            ultima["tiempo_encontrada_s"] if ultima["tiempo_encontrada_s"] is not None else ""
        ),
        "duracion_ultima_solucion": ultima["duracion_plan"],
        "pasos_ultima_solucion": ultima["pasos_plan"],
        "mejora_duracion": primera["duracion_plan"] - ultima["duracion_plan"],
        "mejora_pasos": primera["pasos_plan"] - ultima["pasos_plan"],
        "timeout_s": LIMITE_TIEMPO,
        "log": ejecucion["log"],
    }



def construir_fila_error_generacion(
    drones: int,
    carriers: int,
    n: int,
    problema: str
) -> Dict[str, object]:
    return {
        "drones": drones,
        "transportadores": carriers,
        "n": n,
        "problema": problema,
        "motivo_final": "error_generacion",
        "returncode": "error",
        "num_soluciones": 0,
        "tiempo_primera_solucion_s": "",
        "duracion_primera_solucion": "",
        "pasos_primera_solucion": "",
        "tiempo_ultima_solucion_s": "",
        "duracion_ultima_solucion": "",
        "pasos_ultima_solucion": "",
        "mejora_duracion": "",
        "mejora_pasos": "",
        "timeout_s": LIMITE_TIEMPO,
        "log": "",
    }


# =========================================================
# RESUMEN
# =========================================================


def num_soluciones_fila(fila: Dict[str, object]) -> int:
    try:
        return int(str(fila["num_soluciones"]))
    except (ValueError, TypeError, KeyError):
        return 0



def fila_tiene_solucion(fila: Dict[str, object]) -> bool:
    return num_soluciones_fila(fila) > 0



def filas_configuracion(
    filas_detalladas: List[Dict[str, object]],
    drones: int,
    carriers: int
) -> List[Dict[str, object]]:
    filtradas = [
        f for f in filas_detalladas
        if int(f["drones"]) == drones and int(f["transportadores"]) == carriers
    ]
    return sorted(filtradas, key=lambda r: int(r["n"]))



def recalcular_resumen_config(
    filas_detalladas: List[Dict[str, object]],
    drones: int,
    carriers: int
) -> Dict[str, object]:
    filas = filas_configuracion(filas_detalladas, drones, carriers)

    ultimo_ok_sin_timeout = None
    ultimo_con_solucion = None
    primer_fallo = None

    for fila in filas:
        if fila["motivo_final"] == "ok":
            ultimo_ok_sin_timeout = fila

        if fila_tiene_solucion(fila):
            ultimo_con_solucion = fila
        elif primer_fallo is None:
            primer_fallo = fila

    return {
        "drones": drones,
        "transportadores": carriers,
        "max_n_sin_timeout": (
            ultimo_ok_sin_timeout["n"] if ultimo_ok_sin_timeout else ""
        ),
        "problema_max_sin_timeout": (
            ultimo_ok_sin_timeout["problema"] if ultimo_ok_sin_timeout else ""
        ),
        "max_n_con_alguna_solucion": (
            ultimo_con_solucion["n"] if ultimo_con_solucion else ""
        ),
        "problema_max_con_alguna_solucion": (
            ultimo_con_solucion["problema"] if ultimo_con_solucion else ""
        ),
        "timeout_o_fallo_en_n": (
            primer_fallo["n"] if primer_fallo else ""
        ),
        "motivo_ultimo_intento": (
            primer_fallo["motivo_final"] if primer_fallo
            else (ultimo_con_solucion["motivo_final"] if ultimo_con_solucion else "")
        ),
    }



def actualizar_resumen_global(
    filas_resumen: List[Dict[str, object]],
    resumen_config: Dict[str, object]
) -> List[Dict[str, object]]:
    nuevas = []
    reemplazado = False

    for fila in filas_resumen:
        if int(fila["drones"]) == int(resumen_config["drones"]) and int(fila["transportadores"]) == int(resumen_config["transportadores"]):
            nuevas.append(resumen_config)
            reemplazado = True
        else:
            nuevas.append(fila)

    if not reemplazado:
        nuevas.append(resumen_config)

    return nuevas


# =========================================================
# REANUDACION Y RESET
# =========================================================


def clave_detallado(fila: Dict[str, object]) -> Tuple[int, int, int]:
    return (int(fila["drones"]), int(fila["transportadores"]), int(fila["n"]))



def resetear_configuracion(
    filas_detalladas: List[Dict[str, object]],
    filas_resumen: List[Dict[str, object]],
    drones: int,
    carriers: int
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    nuevas_detalladas = [
        f for f in filas_detalladas
        if not (int(f["drones"]) == drones and int(f["transportadores"]) == carriers)
    ]

    nuevas_resumen = [
        f for f in filas_resumen
        if not (int(f["drones"]) == drones and int(f["transportadores"]) == carriers)
    ]

    ruta_logs = os.path.join(CARPETA_RESULTADOS, f"logs_d{drones}_r{carriers}")
    if os.path.exists(ruta_logs):
        shutil.rmtree(ruta_logs)

    return nuevas_detalladas, nuevas_resumen


# =========================================================
# IMPRESION
# =========================================================


def imprimir_fila(fila: Dict[str, object], origen: str) -> None:
    motivo = str(fila["motivo_final"]).upper()

    if fila_tiene_solucion(fila):
        print(
            f"  [{origen}] {motivo} | soluciones={fila['num_soluciones']} "
            f"| t_primera={fila['tiempo_primera_solucion_s']} "
            f"| dur_primera={fila['duracion_primera_solucion']} "
            f"| pasos_primera={fila['pasos_primera_solucion']} "
            f"| t_ultima={fila['tiempo_ultima_solucion_s']} "
            f"| dur_ultima={fila['duracion_ultima_solucion']} "
            f"| pasos_ultima={fila['pasos_ultima_solucion']}"
        )
    else:
        print(f"  [{origen}] {motivo} | sin soluciones")


# =========================================================
# EJECUCION DE UN N Y GUARDADO INMEDIATO
# =========================================================


def obtener_o_ejecutar_fila(
    drones: int,
    carriers: int,
    n: int,
    regenerar: bool,
    filas_detalladas: List[Dict[str, object]],
    filas_resumen: List[Dict[str, object]],
    indice_existentes: Dict[Tuple[int, int, int], Dict[str, object]],
) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]]]:
    clave = (drones, carriers, n)

    print(f"Probando n = {n} ...")

    if clave in indice_existentes:
        fila = indice_existentes[clave]
        imprimir_fila(fila, "existente")
        return fila, filas_detalladas, filas_resumen

    problema = nombre_problema(drones, carriers, n)

    try:
        generar_problema(drones, carriers, n, regenerar)
    except subprocess.CalledProcessError:
        fila = construir_fila_error_generacion(drones, carriers, n, problema)
    else:
        ejecucion = ejecutar_optic(problema, drones, carriers, n)
        fila = construir_fila_detallada(drones, carriers, n, problema, ejecucion)

    filas_detalladas.append(fila)
    indice_existentes[clave] = fila
    imprimir_fila(fila, "nuevo")

    resumen_config = recalcular_resumen_config(filas_detalladas, drones, carriers)
    filas_resumen = actualizar_resumen_global(filas_resumen, resumen_config)

    guardar_csv_detallado(filas_detalladas)
    guardar_csv_resumen(filas_resumen)

    return fila, filas_detalladas, filas_resumen


# =========================================================
# BENCHMARK 
# =========================================================


def benchmark_configuracion(
    drones: int,
    carriers: int,
    max_n: int,
    regenerar: bool,
    filas_detalladas: List[Dict[str, object]],
    filas_resumen: List[Dict[str, object]],
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    print("\n" + "=" * 80)
    print(f"CONFIGURACION: {drones} dron(es), {carriers} transportador(es)")
    print("=" * 80)

    indice_existentes = {
        clave_detallado(f): f for f in filas_detalladas
    }

    ultimo_ok: Optional[Dict[str, object]] = None
    primer_fallo: Optional[Dict[str, object]] = None

    # -----------------------------------------------------
    # FASE 1: barrido grueso de 10 en 10
    # -----------------------------------------------------
    print(f"Barrido grueso: saltos de {SALTO_GRUESO} en {SALTO_GRUESO}")

    n = INICIO_N
    while n <= max_n:
        fila, filas_detalladas, filas_resumen = obtener_o_ejecutar_fila(
            drones=drones,
            carriers=carriers,
            n=n,
            regenerar=regenerar,
            filas_detalladas=filas_detalladas,
            filas_resumen=filas_resumen,
            indice_existentes=indice_existentes,
        )

        if fila_tiene_solucion(fila):
            ultimo_ok = fila
            n += SALTO_GRUESO
        else:
            primer_fallo = fila
            break

    # Si no ha habido ningun fallo hasta max_n, terminamos la configuracion.
    if primer_fallo is None:
        resumen_final = recalcular_resumen_config(filas_detalladas, drones, carriers)
        filas_resumen = actualizar_resumen_global(filas_resumen, resumen_final)
        guardar_csv_detallado(filas_detalladas)
        guardar_csv_resumen(filas_resumen)

        print(
            f"\nResumen config d={drones}, r={carriers}: "
            f"max_n_sin_timeout={resumen_final['max_n_sin_timeout']} | "
            f"max_n_con_alguna_solucion={resumen_final['max_n_con_alguna_solucion']} | "
            f"timeout_o_fallo_en_n={resumen_final['timeout_o_fallo_en_n']} | "
            f"motivo_ultimo_intento={resumen_final['motivo_ultimo_intento']}"
        )
        return filas_detalladas, filas_resumen

    # Si ni siquiera el primero tiene solucion, no hay nada que refinar.
    if ultimo_ok is None:
        print("  -> parada: ningun problema probado tiene solucion dentro de 60 s")
        resumen_final = recalcular_resumen_config(filas_detalladas, drones, carriers)
        filas_resumen = actualizar_resumen_global(filas_resumen, resumen_final)
        guardar_csv_detallado(filas_detalladas)
        guardar_csv_resumen(filas_resumen)

        print(
            f"\nResumen config d={drones}, r={carriers}: "
            f"max_n_sin_timeout={resumen_final['max_n_sin_timeout']} | "
            f"max_n_con_alguna_solucion={resumen_final['max_n_con_alguna_solucion']} | "
            f"timeout_o_fallo_en_n={resumen_final['timeout_o_fallo_en_n']} | "
            f"motivo_ultimo_intento={resumen_final['motivo_ultimo_intento']}"
        )
        return filas_detalladas, filas_resumen

    # -----------------------------------------------------
    # FASE 2: retroceso de 5
    # -----------------------------------------------------
    n_ok = int(ultimo_ok["n"])
    n_fallo = int(primer_fallo["n"])

    n_intermedio = n_fallo - RETROCESO_INTERMEDIO

    # Si el hueco es pequeno, refinamos directamente de 1 en 1.
    if n_intermedio <= n_ok:
        print(f"Refinado directo: {n_ok + 1}..{n_fallo - 1}")
        for n_ref in range(n_ok + 1, n_fallo):
            fila, filas_detalladas, filas_resumen = obtener_o_ejecutar_fila(
                drones=drones,
                carriers=carriers,
                n=n_ref,
                regenerar=regenerar,
                filas_detalladas=filas_detalladas,
                filas_resumen=filas_resumen,
                indice_existentes=indice_existentes,
            )

            if fila_tiene_solucion(fila):
                ultimo_ok = fila
            else:
                print("  -> parada: primer problema sin solucion dentro de 60 s")
                break
    else:
        print(f"Comprobacion intermedia: retroceso de {RETROCESO_INTERMEDIO} hasta n = {n_intermedio}")

        fila_intermedia, filas_detalladas, filas_resumen = obtener_o_ejecutar_fila(
            drones=drones,
            carriers=carriers,
            n=n_intermedio,
            regenerar=regenerar,
            filas_detalladas=filas_detalladas,
            filas_resumen=filas_resumen,
            indice_existentes=indice_existentes,
        )

        # -------------------------------------------------
        # FASE 3A: si n_intermedio funciona, avanzamos de 1 en 1
        # -------------------------------------------------
        if fila_tiene_solucion(fila_intermedia):
            ultimo_ok = fila_intermedia
            print(f"Refinado ascendente de 1 en 1: {n_intermedio + 1}..{n_fallo - 1}")

            for n_ref in range(n_intermedio + 1, n_fallo):
                fila, filas_detalladas, filas_resumen = obtener_o_ejecutar_fila(
                    drones=drones,
                    carriers=carriers,
                    n=n_ref,
                    regenerar=regenerar,
                    filas_detalladas=filas_detalladas,
                    filas_resumen=filas_resumen,
                    indice_existentes=indice_existentes,
                )

                if fila_tiene_solucion(fila):
                    ultimo_ok = fila
                else:
                    print("  -> parada: primer problema sin solucion dentro de 60 s")
                    break

        # -------------------------------------------------
        # FASE 3B: si n_intermedio falla, retrocedemos de 1 en 1
        # -------------------------------------------------
        else:
            print(f"Refinado descendente de 1 en 1: {n_intermedio - 1}..{n_ok + 1}")

            for n_ref in range(n_intermedio - 1, n_ok, -1):
                fila, filas_detalladas, filas_resumen = obtener_o_ejecutar_fila(
                    drones=drones,
                    carriers=carriers,
                    n=n_ref,
                    regenerar=regenerar,
                    filas_detalladas=filas_detalladas,
                    filas_resumen=filas_resumen,
                    indice_existentes=indice_existentes,
                )

                if fila_tiene_solucion(fila):
                    ultimo_ok = fila
                    print("  -> frontera localizada")
                    break

    resumen_final = recalcular_resumen_config(filas_detalladas, drones, carriers)
    filas_resumen = actualizar_resumen_global(filas_resumen, resumen_final)

    guardar_csv_detallado(filas_detalladas)
    guardar_csv_resumen(filas_resumen)

    print(
        f"\nResumen config d={drones}, r={carriers}: "
        f"max_n_sin_timeout={resumen_final['max_n_sin_timeout']} | "
        f"max_n_con_alguna_solucion={resumen_final['max_n_con_alguna_solucion']} | "
        f"timeout_o_fallo_en_n={resumen_final['timeout_o_fallo_en_n']} | "
        f"motivo_ultimo_intento={resumen_final['motivo_ultimo_intento']}"
    )

    return filas_detalladas, filas_resumen


# =========================================================
# MAIN
# =========================================================


def main():
    args = parse_args()

    if not os.path.exists(DOMINIO):
        print(f"Error: no existe {DOMINIO}")
        return

    if not os.path.exists(GENERADOR):
        print(f"Error: no existe {GENERADOR}")
        return

    filas_detalladas = cargar_csv_detallado()
    filas_resumen = cargar_csv_resumen()

    if args.drones is not None or args.carriers is not None:
        if args.drones is None or args.carriers is None:
            print("Si indicas una configuracion concreta, debes pasar --drones y --carriers")
            return
        configuraciones = [(args.drones, args.carriers)]
    else:
        configuraciones = CONFIGURACIONES

    if args.reset_config:
        if len(configuraciones) != 1:
            print("--reset-config solo debe usarse cuando ejecutas una unica configuracion")
            return

        d, r = configuraciones[0]
        filas_detalladas, filas_resumen = resetear_configuracion(
            filas_detalladas, filas_resumen, d, r
        )
        guardar_csv_detallado(filas_detalladas)
        guardar_csv_resumen(filas_resumen)

    print("BENCHMARK PARTE 3 - DEFINITIVO")
    print("Optic | acciones durativas | primera y ultima solucion por problema")
    print("Criterio: exito = al menos una solucion dentro de 60 s")
    print(
        f"Metodologia: barrido grueso cada {SALTO_GRUESO}, "
        f"retroceso de {RETROCESO_INTERMEDIO}, refinado final de 1 en 1"
    )
    print(f"CSV detallado unico: {CSV_DETALLADO}")
    print(f"CSV resumen unico: {CSV_RESUMEN}")

    for drones, carriers in configuraciones:
        filas_detalladas, filas_resumen = benchmark_configuracion(
            drones=drones,
            carriers=carriers,
            max_n=args.max_n,
            regenerar=args.regen or REGENERAR_PROBLEMAS,
            filas_detalladas=filas_detalladas,
            filas_resumen=filas_resumen,
        )

    print("\n" + "=" * 80)
    print("Benchmark terminado.")
    print(f"CSV detallado: {CSV_DETALLADO}")
    print(f"CSV resumen: {CSV_RESUMEN}")
    print(f"Logs: {CARPETA_RESULTADOS}/logs_d*_r*")


if __name__ == "__main__":
    main()
