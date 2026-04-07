(define (problem problem_d1_r1_l6_p6_c6_g6)
(:domain emergency-services-transporters)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
	loc5 - location
	loc6 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
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
	(at-crate crate6 depot)
	(at-person person1 loc3)
	(at-person person2 loc2)
	(at-person person3 loc5)
	(at-person person4 loc5)
	(at-person person5 loc6)
	(at-person person6 loc3)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 food)
	(crate-content crate4 food)
	(crate-content crate5 medicine)
	(crate-content crate6 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (total-cost) 0)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 76)
	(= (fly-cost depot loc2) 182)
	(= (fly-cost depot loc3) 147)
	(= (fly-cost depot loc4) 40)
	(= (fly-cost depot loc5) 134)
	(= (fly-cost depot loc6) 149)
	(= (fly-cost loc1 depot) 76)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 123)
	(= (fly-cost loc1 loc3) 107)
	(= (fly-cost loc1 loc4) 42)
	(= (fly-cost loc1 loc5) 70)
	(= (fly-cost loc1 loc6) 90)
	(= (fly-cost loc2 depot) 182)
	(= (fly-cost loc2 loc1) 123)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 52)
	(= (fly-cost loc2 loc4) 144)
	(= (fly-cost loc2 loc5) 148)
	(= (fly-cost loc2 loc6) 34)
	(= (fly-cost loc3 depot) 147)
	(= (fly-cost loc3 loc1) 107)
	(= (fly-cost loc3 loc2) 52)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 113)
	(= (fly-cost loc3 loc5) 155)
	(= (fly-cost loc3 loc6) 40)
	(= (fly-cost loc4 depot) 40)
	(= (fly-cost loc4 loc1) 42)
	(= (fly-cost loc4 loc2) 144)
	(= (fly-cost loc4 loc3) 113)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 108)
	(= (fly-cost loc4 loc6) 111)
	(= (fly-cost loc5 depot) 134)
	(= (fly-cost loc5 loc1) 70)
	(= (fly-cost loc5 loc2) 148)
	(= (fly-cost loc5 loc3) 155)
	(= (fly-cost loc5 loc4) 108)
	(= (fly-cost loc5 loc5) 1)
	(= (fly-cost loc5 loc6) 124)
	(= (fly-cost loc6 depot) 149)
	(= (fly-cost loc6 loc1) 90)
	(= (fly-cost loc6 loc2) 34)
	(= (fly-cost loc6 loc3) 40)
	(= (fly-cost loc6 loc4) 111)
	(= (fly-cost loc6 loc5) 124)
	(= (fly-cost loc6 loc6) 1)
)
(:goal (and
	(has-content person1 food)
	(has-content person1 medicine)
	(has-content person2 food)
	(has-content person3 food)
	(has-content person5 food)
	(has-content person6 medicine)
	))
(:metric minimize (total-cost))
)
