(define (problem problem_d1_r1_l7_p7_c7_g7)
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
	loc7 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
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
	(at-crate crate7 depot)
	(at-person person1 loc5)
	(at-person person2 loc3)
	(at-person person3 loc2)
	(at-person person4 loc1)
	(at-person person5 loc1)
	(at-person person6 loc5)
	(at-person person7 loc2)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 food)
	(crate-content crate4 food)
	(crate-content crate5 food)
	(crate-content crate6 food)
	(crate-content crate7 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (total-cost) 0)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 104)
	(= (fly-cost depot loc2) 161)
	(= (fly-cost depot loc3) 82)
	(= (fly-cost depot loc4) 193)
	(= (fly-cost depot loc5) 220)
	(= (fly-cost depot loc6) 250)
	(= (fly-cost depot loc7) 149)
	(= (fly-cost loc1 depot) 104)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 58)
	(= (fly-cost loc1 loc3) 46)
	(= (fly-cost loc1 loc4) 126)
	(= (fly-cost loc1 loc5) 135)
	(= (fly-cost loc1 loc6) 150)
	(= (fly-cost loc1 loc7) 131)
	(= (fly-cost loc2 depot) 161)
	(= (fly-cost loc2 loc1) 58)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 94)
	(= (fly-cost loc2 loc4) 113)
	(= (fly-cost loc2 loc5) 103)
	(= (fly-cost loc2 loc6) 98)
	(= (fly-cost loc2 loc7) 152)
	(= (fly-cost loc3 depot) 82)
	(= (fly-cost loc3 loc1) 46)
	(= (fly-cost loc3 loc2) 94)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 115)
	(= (fly-cost loc3 loc5) 139)
	(= (fly-cost loc3 loc6) 173)
	(= (fly-cost loc3 loc7) 94)
	(= (fly-cost loc4 depot) 193)
	(= (fly-cost loc4 loc1) 126)
	(= (fly-cost loc4 loc2) 113)
	(= (fly-cost loc4 loc3) 115)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 45)
	(= (fly-cost loc4 loc6) 110)
	(= (fly-cost loc4 loc7) 82)
	(= (fly-cost loc5 depot) 220)
	(= (fly-cost loc5 loc1) 135)
	(= (fly-cost loc5 loc2) 103)
	(= (fly-cost loc5 loc3) 139)
	(= (fly-cost loc5 loc4) 45)
	(= (fly-cost loc5 loc5) 1)
	(= (fly-cost loc5 loc6) 68)
	(= (fly-cost loc5 loc7) 125)
	(= (fly-cost loc6 depot) 250)
	(= (fly-cost loc6 loc1) 150)
	(= (fly-cost loc6 loc2) 98)
	(= (fly-cost loc6 loc3) 173)
	(= (fly-cost loc6 loc4) 110)
	(= (fly-cost loc6 loc5) 68)
	(= (fly-cost loc6 loc6) 1)
	(= (fly-cost loc6 loc7) 187)
	(= (fly-cost loc7 depot) 149)
	(= (fly-cost loc7 loc1) 131)
	(= (fly-cost loc7 loc2) 152)
	(= (fly-cost loc7 loc3) 94)
	(= (fly-cost loc7 loc4) 82)
	(= (fly-cost loc7 loc5) 125)
	(= (fly-cost loc7 loc6) 187)
	(= (fly-cost loc7 loc7) 1)
)
(:goal (and
	(has-content person1 food)
	(has-content person2 food)
	(has-content person4 food)
	(has-content person5 food)
	(has-content person6 food)
	(has-content person7 food)
	(has-content person7 medicine)
	))
(:metric minimize (total-cost))
)
