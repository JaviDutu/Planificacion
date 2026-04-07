#!/usr/bin/env python3

########################################################################################
# Problem instance generator skeleton for emergencies drones domain.
# Based on the Linköping University TDDD48 2021 course.
# https://www.ida.liu.se/~TDDD48/labs/2021/lab1/index.en.shtml
#
# You mainly have to change the parts marked as TODO.
#
########################################################################################


from optparse import OptionParser
import random
import math
import sys

########################################################################################
# Hard-coded options
########################################################################################

content_types = ["food", "medicine"]
TRANSPORTER_CAPACITY = 4


########################################################################################
# Random seed
########################################################################################

# Set seed to 0 if you want more predictability...
# random.seed(0);

########################################################################################
# Helper functions
########################################################################################

def distance(location_coords, location_num1, location_num2):
    x1 = location_coords[location_num1][0]
    y1 = location_coords[location_num1][1]
    x2 = location_coords[location_num2][0]
    y2 = location_coords[location_num2][1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def flight_cost(location_coords, location_num1, location_num2):
    return int(distance(location_coords, location_num1, location_num2)) + 1


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

    print()
    print("Types\tQuantities")
    for x in range(len(num_crates_with_contents)):
        if num_crates_with_contents[x] > 0:
            print(content_types[x] + "\t " + str(num_crates_with_contents[x]))

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
    location_coords = [(0, 0)]
    for x in range(1, options.locations + 1):
        location_coords.append((random.randint(1, 200), random.randint(1, 200)))

    print("Location positions", location_coords)
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
# Main program
########################################################################################

def main():
    parser = OptionParser(usage='python generator.py [-help] options...')
    parser.add_option('-d', '--drones', metavar='NUM', dest='drones', action='store', type=int, help='the number of drones')
    parser.add_option('-r', '--carriers', metavar='NUM', type=int, dest='carriers',
                      help='the number of carriers, for later labs; use 0 for no carriers')
    parser.add_option('-l', '--locations', metavar='NUM', type=int, dest='locations',
                      help='the number of locations apart from the depot ')
    parser.add_option('-p', '--persons', metavar='NUM', type=int, dest='persons', help='the number of persons')
    parser.add_option('-c', '--crates', metavar='NUM', type=int, dest='crates', help='the number of crates available')
    parser.add_option('-g', '--goals', metavar='NUM', type=int, dest='goals',
                      help='the number of crates assigned in the goal')

    (options, args) = parser.parse_args()

    if options.drones is None:
        print("You must specify --drones (use --help for help)")
        sys.exit(1)

    if options.carriers is None:
        print("You must specify --carriers (use --help for help)")
        sys.exit(1)

    if options.locations is None:
        print("You must specify --locations (use --help for help)")
        sys.exit(1)

    if options.persons is None:
        print("You must specify --persons (use --help for help)")
        sys.exit(1)

    if options.crates is None:
        print("You must specify --crates (use --help for help)")
        sys.exit(1)

    if options.goals is None:
        print("You must specify --goals (use --help for help)")
        sys.exit(1)

    if options.goals > options.crates:
        print("Cannot have more goals than crates")
        sys.exit(1)

    if len(content_types) > options.crates:
        print("Cannot have more content types than crates:", content_types)
        sys.exit(1)

    if options.goals > len(content_types) * options.persons:
        print("For", options.persons, "persons, you can have at most", len(content_types) * options.persons, "goals")
        sys.exit(1)

    if options.carriers < 1:
        print("There must be at least 1 transporter")
        sys.exit(1)

    print("Drones\t\t", options.drones)
    print("Carriers\t", options.carriers)
    print("Locations\t", options.locations)
    print("Persons\t\t", options.persons)
    print("Crates\t\t", options.crates)
    print("Goals\t\t", options.goals)

    drone = []
    person = []
    crate = []
    carrier = []
    location = []
    nums = []

    location.append("depot")
    for x in range(options.locations):
        location.append("loc" + str(x + 1))
    for x in range(options.drones):
        drone.append("drone" + str(x + 1))
    for x in range(options.carriers):
        carrier.append("transporter" + str(x + 1))
    for x in range(options.persons):
        person.append("person" + str(x + 1))
    for x in range(options.crates):
        crate.append("crate" + str(x + 1))
    for x in range(TRANSPORTER_CAPACITY + 1):
        nums.append("n" + str(x))

    crates_with_contents = setup_content_types(options)
    location_coords = setup_location_coords(options)
    need = setup_person_needs(options, crates_with_contents)

    person_locations = []
    for x in range(options.persons):
        rand_loc = random.randint(1, options.locations)
        person_locations.append(location[rand_loc])

    problem_name = "problem_d" + str(options.drones) + "_r" + str(options.carriers) + \
                   "_l" + str(options.locations) + "_p" + str(options.persons) + "_c" + str(options.crates) + \
                   "_g" + str(options.goals)

    with open(problem_name + ".pddl", 'w') as f:
        f.write("(define (problem " + problem_name + ")\n")
        f.write("(:domain emergency-services-transporters)\n")
        f.write("(:objects\n")

        ######################################################################
        # Write objects

        for x in drone:
            f.write("\t" + x + " - drone\n")

        for x in location:
            f.write("\t" + x + " - location\n")

        for x in crate:
            f.write("\t" + x + " - crate\n")

        for x in content_types:
            f.write("\t" + x + " - content\n")

        for x in person:
            f.write("\t" + x + " - person\n")

        for x in carrier:
            f.write("\t" + x + " - transporter\n")

        for x in nums:
            f.write("\t" + x + " - num\n")

        f.write(")\n")

        ######################################################################
        # Generate an initial state

        f.write("(:init\n")

        for x in drone:
            f.write("\t(at-drone " + x + " depot)\n")
            f.write("\t(hand-empty " + x + ")\n")

        for x in carrier:
            f.write("\t(at-transporter " + x + " depot)\n")
            f.write("\t(free-slots " + x + " n" + str(TRANSPORTER_CAPACITY) + ")\n")

        for x in crate:
            f.write("\t(at-crate " + x + " depot)\n")

        for i in range(options.persons):
            f.write("\t(at-person " + person[i] + " " + person_locations[i] + ")\n")

        for content_index in range(len(content_types)):
            for crate_name in crates_with_contents[content_index]:
                f.write("\t(crate-content " + crate_name + " " + content_types[content_index] + ")\n")

        for i in range(TRANSPORTER_CAPACITY):
            f.write("\t(siguiente n" + str(i) + " n" + str(i + 1) + ")\n")

        f.write(")\n")

        ######################################################################
        # Write Goals

        f.write("(:goal (and\n")

        for x in range(options.persons):
            for y in range(len(content_types)):
                if need[x][y]:
                    person_name = person[x]
                    content_name = content_types[y]
                    f.write("\t(has-content " + person_name + " " + content_name + ")\n")

        f.write("\t))\n")
        f.write(")\n")


if __name__ == '__main__':
    main()