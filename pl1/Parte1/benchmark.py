import subprocess
import re
import sys

# Configuración
domain_file = "domain.pddl"
problem_file = "problem_gen.pddl"
# Aumentamos el tamaño máximo para intentar llegar al minuto
max_size = 200  
time_limit = 60 # 1 minuto límite

print(f"{'Tamaño':<10} | {'Tiempo (s)':<15} | {'Pasos':<15} | {'Resultado'}")
print("-" * 65)

# Acciones de tu dominio para contar los pasos correctamente
action_names = ["fly", "pick-up", "deliver"]

for size in range(5, max_size + 1, 5): # Saltamos de 5 en 5 para ir más rápido
    
    # 1. Generar el problema
    gen_cmd = [
        "python3", "generate-problem.py",
        "-d", "1", "-r", "0",
        "-l", str(size),
        "-p", str(size),
        "-c", str(size),
        "-g", str(size)
    ]
    
    try:
        subprocess.run(gen_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print(f"Error generando problema tamaño {size}")
        break

    # 2. Ejecutar FF
    run_cmd = ["planutils", "run", "ff", domain_file, problem_file]

    try:
        result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=time_limit)
        output = result.stdout

        # 3. Analizar salida
        if "found legal plan" in output:
            # Buscar tiempo
            time_match = re.search(r"(\d+\.\d+) seconds total time", output)
            time_val = float(time_match.group(1)) if time_match else 0.0

            # CONTAR PASOS REALES: Contamos cuántas veces aparecen las acciones
            steps = 0
            for action in action_names:
                # Usamos ignorecase porque FF suele devolver en mayúsculas (FLY, PICK-UP...)
                steps += len(re.findall(action, output, re.IGNORECASE))
            
            print(f"{size:<10} | {time_val:<15.4f} | {steps:<15} | OK")
        
        else:
            print(f"{size:<10} | {'-':<15} | {'-':<15} | Fallo (Sin solución)")

    except subprocess.TimeoutExpired:
        print(f"{size:<10} | {'> 60.00':<15} | {'-':<15} | TIMEOUT (Límite alcanzado)")
        print("-" * 65)
        print(f"¡LÍMITE ENCONTRADO! El tamaño máximo resuelto en <1 min es: {size - 5}")
        break
    
    except FileNotFoundError:
        print("Error: planutils no encontrado.")
        break