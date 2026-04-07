(define (problem problem_d1_r1_l5_p5_c5_g5)
(:domain emergency-services-transporters)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
	loc5 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	transporter1 - transporter
	n0 - num
	n1 - num
	n2 - num
	n3 - num
	n4 - num
)
(:init
	(at-drone drone1 depot)
	(hand-empty drone1)
	(at-transporter transporter1 depot)
	(free-slots transporter1 n4)
	(at-crate crate1 depot)
	(at-crate crate2 depot)
	(at-crate crate3 depot)
	(at-crate crate4 depot)
	(at-crate crate5 depot)
	(at-person person1 loc4)
	(at-person person2 loc4)
	(at-person person3 loc4)
	(at-person person4 loc1)
	(at-person person5 loc2)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 medicine)
	(crate-content crate4 medicine)
	(crate-content crate5 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (total-cost) 0)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 72)
	(= (fly-cost depot loc2) 173)
	(= (fly-cost depot loc3) 139)
	(= (fly-cost depot loc4) 217)
	(= (fly-cost depot loc5) 226)
	(= (fly-cost loc1 depot) 72)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 147)
	(= (fly-cost loc1 loc3) 125)
	(= (fly-cost loc1 loc4) 169)
	(= (fly-cost loc1 loc5) 178)
	(= (fly-cost loc2 depot) 173)
	(= (fly-cost loc2 loc1) 147)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 40)
	(= (fly-cost loc2 loc4) 68)
	(= (fly-cost loc2 loc5) 77)
	(= (fly-cost loc3 depot) 139)
	(= (fly-cost loc3 loc1) 125)
	(= (fly-cost loc3 loc2) 40)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 104)
	(= (fly-cost loc3 loc5) 114)
	(= (fly-cost loc4 depot) 217)
	(= (fly-cost loc4 loc1) 169)
	(= (fly-cost loc4 loc2) 68)
	(= (fly-cost loc4 loc3) 104)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 11)
	(= (fly-cost loc5 depot) 226)
	(= (fly-cost loc5 loc1) 178)
	(= (fly-cost loc5 loc2) 77)
	(= (fly-cost loc5 loc3) 114)
	(= (fly-cost loc5 loc4) 11)
	(= (fly-cost loc5 loc5) 1)
)
(:goal (and
	(has-content person1 medicine)
	(has-content person2 food)
	(has-content person2 medicine)
	(has-content person3 food)
	(has-content person4 medicine)
	))
(:metric minimize (total-cost))
)
