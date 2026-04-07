(define (problem problem_d2_r2_l2_p2_c2_g2)
(:domain emergency-services-transporters)
(:objects
	drone1 - drone
	drone2 - drone
	depot - location
	loc1 - location
	loc2 - location
	crate1 - crate
	crate2 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	transporter1 - transporter
	transporter2 - transporter
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
	(at-transporter transporter1 depot)
	(free-slots transporter1 n4)
	(transporter-free transporter1)
	(at-transporter transporter2 depot)
	(free-slots transporter2 n4)
	(transporter-free transporter2)
	(at-crate crate1 depot)
	(at-crate crate2 depot)
	(at-person person1 loc1)
	(person-free person1)
	(at-person person2 loc2)
	(person-free person2)
	(crate-content crate1 food)
	(crate-content crate2 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 223)
	(= (fly-cost depot loc2) 68)
	(= (fly-cost loc1 depot) 223)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 189)
	(= (fly-cost loc2 depot) 68)
	(= (fly-cost loc2 loc1) 189)
	(= (fly-cost loc2 loc2) 1)
)
(:goal (and
	(has-content person2 food)
	(has-content person2 medicine)
	))
(:metric minimize (total-time))
)
