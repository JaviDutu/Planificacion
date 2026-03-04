import subprocess
import re
import sys
import os

# --- CONFIGURACIÓN ---
DOMAIN_FILE = "domain.pddl"
PROBLEM_FILE = "problem_gen.pddl"
TIME_LIMIT = 60 

def run_experiment(search, heuristic=None, size=2):
    # 1. Generar el problema
    gen_cmd = [
        sys.executable, "generate-problem.py",
        "-d", "1", "-r", "0", 
        "-l", str(size), "-p", str(size), "-c", str(size), "-g", str(size)
    ]
    subprocess.run(gen_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 2. Preparar comando pyperplan con los nombres correctos (gbf, ehs)
    cmd = ["pyperplan", "-s", search]
    if heuristic:
        cmd.extend(["-H", heuristic])
    cmd.extend([DOMAIN_FILE, PROBLEM_FILE])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIME_LIMIT)
        output = result.stdout
        
        # Regex mejorado para capturar tiempo y pasos
        time_match = re.search(r"Search time:\s+([\d\.]+)", output)
        steps_match = re.search(r"Plan length:\s+(\d+)", output)
        
        if time_match and steps_match:
            return float(time_match.group(1)), int(steps_match.group(1)), "OK"
        return None, None, "ERROR_SALIDA"
            
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"

def print_header(title):
    print(f"\n{'='*85}")
    print(f" {title}")
    print(f"{'='*85}")
    print(f"{'Algoritmo':<10} | {'Heurística':<12} | {'Tam.':<5} | {'Tiempo':<10} | {'Pasos':<6} | {'Óptimo':<6} | {'Estado'}")
    print("-" * 85)

# --- EJECUCIÓN ---

# 1.3.1: Comparativa General (Corregido 'gbfs' -> 'gbf')
print_header("1.3.1: BÚSQUEDA DE TAMAÑO MÁXIMO")
configs_p1 = [
    ("bfs", None, True), 
    ("ids", None, True), 
    ("astar", "hmax", True), 
    ("gbf", "hmax", False) # Antes era gbfs
]

max_sizes = {"gbf": 2, "astar": 2}

for search, heur, is_optimal in configs_p1:
    for size in range(2, 50): 
        t, steps, status = run_experiment(search, heur, size)
        h_name = heur if heur else "Ninguna"
        print(f"{search:<10} | {h_name:<12} | {size:<5} | {f'{t:.3f}s' if t else '-':<10} | {steps if steps else '-':<6} | {'SÍ' if is_optimal else 'NO':<6} | {status}")
        
        if status == "OK":
            if search == "gbf": max_sizes["gbf"] = size
            if search == "astar": max_sizes["astar"] = size
        else: break

# 1.3.2: Heurísticas Satisficing (Corregido 'gbf' y 'ehs')
target_size_sat = max_sizes["gbf"]
print_header(f"1.3.2: HEURÍSTICAS SATISFICING (Tamaño fijo: {target_size_sat})")
configs_p2 = [
    ("gbf", "hmax"), ("gbf", "hadd"), ("gbf", "hff"), ("gbf", "landmark"),
    ("ehs", "hmax"), ("ehs", "hadd"), ("ehs", "hff"), ("ehs", "landmark")
]
for search, heur in configs_p2:
    t, steps, status = run_experiment(search, heur, target_size_sat)
    print(f"{search:<10} | {heur:<12} | {target_size_sat:<5} | {f'{t:.3f}s' if t else '-':<10} | {steps if steps else '-':<6} | {'NO':<6} | {status}")

# 1.3.3: Heurísticas Óptimas (Usa el tamaño máximo de A*)
target_size_opt = max_sizes["astar"]
print_header(f"1.3.3: HEURÍSTICAS ÓPTIMAS (Tamaño fijo: {target_size_opt})")
configs_p3 = [("bfs", None), ("ids", None), ("astar", "hmax"), ("astar", "lmcut")]
for search, heur in configs_p3:
    t, steps, status = run_experiment(search, heur, target_size_opt)
    print(f"{search:<10} | {heur if heur else 'Ninguna':<12} | {target_size_opt:<5} | {f'{t:.3f}s' if t else '-':<10} | {steps if steps else '-':<6} | {'SÍ':<6} | {status}")