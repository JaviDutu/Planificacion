(define (problem problem_d5_r5_l4_p4_c4_g4)
(:domain emergency-services-transporters)
(:objects
	drone1 - drone
	drone2 - drone
	drone3 - drone
	drone4 - drone
	drone5 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	transporter1 - transporter
	transporter2 - transporter
	transporter3 - transporter
	transporter4 - transporter
	transporter5 - transporter
	n0 - num
	n1 - num
	n2 - num
	n3 - num
	n4 - num
)
(:init
	(at-drone drone1 depot)
	(hand-empty drone1)
	(drone-free drone1)
	(at-drone drone2 depot)
	(hand-empty drone2)
	(drone-free drone2)
	(at-drone drone3 depot)
	(hand-empty drone3)
	(drone-free drone3)
	(at-drone drone4 depot)
	(hand-empty drone4)
	(drone-free drone4)
	(at-drone drone5 depot)
	(hand-empty drone5)
	(drone-free drone5)
	(at-transporter transporter1 depot)
	(free-slots transporter1 n4)
	(transporter-free transporter1)
	(at-transporter transporter2 depot)
	(free-slots transporter2 n4)
	(transporter-free transporter2)
	(at-transporter transporter3 depot)
	(free-slots transporter3 n4)
	(transporter-free transporter3)
	(at-transporter transporter4 depot)
	(free-slots transporter4 n4)
	(transporter-free transporter4)
	(at-transporter transporter5 depot)
	(free-slots transporter5 n4)
	(transporter-free transporter5)
	(at-crate crate1 depot)
	(at-crate crate2 depot)
	(at-crate crate3 depot)
	(at-crate crate4 depot)
	(at-person person1 loc2)
	(person-free person1)
	(at-person person2 loc3)
	(person-free person2)
	(at-person person3 loc1)
	(person-free person3)
	(at-person person4 loc1)
	(person-free person4)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 medicine)
	(crate-content crate4 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 223)
	(= (fly-cost depot loc2) 68)
	(= (fly-cost depot loc3) 182)
	(= (fly-cost depot loc4) 131)
	(= (fly-cost loc1 depot) 223)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 189)
	(= (fly-cost loc1 loc3) 67)
	(= (fly-cost loc1 loc4) 96)
	(= (fly-cost loc2 depot) 68)
	(= (fly-cost loc2 loc1) 189)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 134)
	(= (fly-cost loc2 loc4) 94)
	(= (fly-cost loc3 depot) 182)
	(= (fly-cost loc3 loc1) 67)
	(= (fly-cost loc3 loc2) 134)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 55)
	(= (fly-cost loc4 depot) 131)
	(= (fly-cost loc4 loc1) 96)
	(= (fly-cost loc4 loc2) 94)
	(= (fly-cost loc4 loc3) 55)
	(= (fly-cost loc4 loc4) 1)
)
(:goal (and
	(has-content person1 medicine)
	(has-content person2 food)
	(has-content person3 food)
	(has-content person4 medicine)
	))
(:metric minimize (total-time))
)
