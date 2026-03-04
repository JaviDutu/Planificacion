#!/usr/bin/env python3

########################################################################################
# Generador de problemas para Dominio de Emergencias (Ejercicio 1.2)
# Adaptado para emergency-services (PDDL)
########################################################################################

from optparse import OptionParser
import random
import math
import sys

########################################################################################
# Opciones
########################################################################################

# Tipos de contenido (coinciden con el dominio)
content_types = ["food", "medicine"]

########################################################################################
# Funciones auxiliares
########################################################################################

def setup_content_types(options):
    while True:
        num_crates_with_contents = []
        crates_left = options.crates
        for x in range(len(content_types) - 1):
            types_after_this = len(content_types) - x - 1
            max_now = crates_left - types_after_this
            num = random.randint(1, max_now)
            num_crates_with_contents.append(num)
            crates_left -= num
        num_crates_with_contents.append(crates_left)

        maxgoals = sum(min(num_crates, options.persons) for num_crates in num_crates_with_contents)

        if options.goals <= maxgoals:
            break

    # Debug info
    # print("Types\tQuantities")
    # for x in range(len(num_crates_with_contents)):
    #     if num_crates_with_contents[x] > 0:
    #         print(content_types[x] + "\t " + str(num_crates_with_contents[x]))

    crates_with_contents = []
    counter = 1
    for x in range(len(content_types)):
        crates = []
        for y in range(num_crates_with_contents[x]):
            crates.append("crate" + str(counter))
            counter += 1
        crates_with_contents.append(crates)

    return crates_with_contents

def setup_location_coords(options):
    location_coords = [(0, 0)]  # Deposito
    for x in range(1, options.locations + 1):
        location_coords.append((random.randint(1, 200), random.randint(1, 200)))
    return location_coords

def setup_person_needs(options, crates_with_contents):
    need = [[False for i in range(len(content_types))] for j in range(options.persons)]
    goals_per_contents = [0 for i in range(len(content_types))]

    for goalnum in range(options.goals):
        generated = False
        while not generated:
            rand_person = random.randint(0, options.persons - 1)
            rand_content = random.randint(0, len(content_types) - 1)
            
            if (goals_per_contents[rand_content] < len(crates_with_contents[rand_content])
                    and not need[rand_person][rand_content]):
                need[rand_person][rand_content] = True
                goals_per_contents[rand_content] += 1
                generated = True
    return need

########################################################################################
# Main
########################################################################################

def main():
    parser = OptionParser(usage='python generator.py [-help] options...')
    parser.add_option('-d', '--drones', metavar='NUM', dest='drones', action='store', type=int, help='number of drones')
    parser.add_option('-r', '--carriers', metavar='NUM', type=int, dest='carriers', help='ignored in this lab')
    parser.add_option('-l', '--locations', metavar='NUM', type=int, dest='locations', help='number of locations (excluding depot)')
    parser.add_option('-p', '--persons', metavar='NUM', type=int, dest='persons', help='number of persons')
    parser.add_option('-c', '--crates', metavar='NUM', type=int, dest='crates', help='number of crates')
    parser.add_option('-g', '--goals', metavar='NUM', type=int, dest='goals', help='number of goals')

    (options, args) = parser.parse_args()

    # Validaciones basicas
    if options.drones is None or options.locations is None or options.persons is None or options.crates is None or options.goals is None:
        print("Error: Faltan argumentos. Usa: -d 1 -r 0 -l 3 -p 3 -c 3 -g 3")
        sys.exit(1)

    if options.crates < len(content_types):
        print(f"Error: El número mínimo de cajas debe ser {len(content_types)}.")
        sys.exit(1)


    # Listas de objetos
    drone = []
    person = []
    crate = []
    location = []

    location.append("depot")
    for x in range(options.locations):
        location.append("loc" + str(x + 1))
    for x in range(options.drones):
        drone.append("drone" + str(x + 1))
    for x in range(options.persons):
        person.append("person" + str(x + 1))
    # Crates se generan dentro de setup_content_types
    
    crates_with_contents = setup_content_types(options)
    
    # Aplanar la lista de cajas para declararlas
    all_crates = []
    for sublist in crates_with_contents:
        for c in sublist:
            all_crates.append(c)

    need = setup_person_needs(options, crates_with_contents)

    # Nombre del archivo de salida
    problem_name = "problem_gen" # Nombre generico o dinamico
    filename = "problem_gen.pddl"

    with open(filename, 'w') as f:
        f.write(f"(define (problem {problem_name})\n")
        f.write("(:domain emergency-services)\n") # IMPORTANTE: Coincide con domain.pddl
        f.write("(:objects\n")

        # 1. DEFINICION DE OBJETOS
        for x in drone:
            f.write("\t" + x + " - drone\n")
        
        for x in location:
            f.write("\t" + x + " - location\n")
            
        for x in all_crates:
            f.write("\t" + x + " - crate\n")
            
        for x in person:
            f.write("\t" + x + " - person\n")
            
        # Tipos fijos
        f.write("\tleft right - arm\n")
        for t in content_types:
            f.write("\t" + t + " - content\n") # OJO: content singular

        f.write(")\n")

        # 2. ESTADO INICIAL
        f.write("(:init\n")

        # Drones en deposito y brazos vacios
        for d in drone:
            f.write(f"\t(at-drone {d} depot)\n")
            f.write(f"\t(hand-empty {d} left)\n")
            f.write(f"\t(hand-empty {d} right)\n")

        # Cajas en deposito y su contenido
        # crates_with_contents es [[c1, c2], [c3]] correspondientes a content_types [food, medicine]
        for idx, content_name in enumerate(content_types):
            for c in crates_with_contents[idx]:
                f.write(f"\t(at-crate {c} depot)\n")
                f.write(f"\t(crate-content {c} {content_name})\n")

        # Personas en localizaciones aleatorias (no depot)
        real_locations = location[1:] # Excluye depot
        for p in person:
            loc = random.choice(real_locations)
            f.write(f"\t(at-person {p} {loc})\n")

        f.write(")\n")

        # 3. METAS
        f.write("(:goal (and\n")

        # Metas de personas (contenido)
        for x in range(options.persons):
            for y in range(len(content_types)):
                if need[x][y]:
                    person_name = person[x]
                    content_name = content_types[y]
                    f.write(f"\t(has-content {person_name} {content_name})\n")

        f.write("))\n")
        f.write(")\n")

    print(f"Generado problema: {filename} con {options.locations} locs, {options.persons} personas, {options.crates} cajas.")

if __name__ == '__main__':
    main()