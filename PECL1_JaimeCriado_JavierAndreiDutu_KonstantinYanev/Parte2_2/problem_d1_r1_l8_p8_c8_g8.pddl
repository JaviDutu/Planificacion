(define (problem problem_d1_r1_l8_p8_c8_g8)
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
	loc8 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	crate8 - crate
	food - content
	medicine - content
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
	person8 - person
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
	(at-crate crate8 depot)
	(at-person person1 loc3)
	(at-person person2 loc7)
	(at-person person3 loc7)
	(at-person person4 loc2)
	(at-person person5 loc6)
	(at-person person6 loc6)
	(at-person person7 loc1)
	(at-person person8 loc7)
	(crate-content crate1 food)
	(crate-content crate2 medicine)
	(crate-content crate3 medicine)
	(crate-content crate4 medicine)
	(crate-content crate5 medicine)
	(crate-content crate6 medicine)
	(crate-content crate7 medicine)
	(crate-content crate8 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (total-cost) 0)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 167)
	(= (fly-cost depot loc2) 109)
	(= (fly-cost depot loc3) 104)
	(= (fly-cost depot loc4) 81)
	(= (fly-cost depot loc5) 176)
	(= (fly-cost depot loc6) 23)
	(= (fly-cost depot loc7) 180)
	(= (fly-cost depot loc8) 206)
	(= (fly-cost loc1 depot) 167)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 59)
	(= (fly-cost loc1 loc3) 164)
	(= (fly-cost loc1 loc4) 109)
	(= (fly-cost loc1 loc5) 26)
	(= (fly-cost loc1 loc6) 159)
	(= (fly-cost loc1 loc7) 118)
	(= (fly-cost loc1 loc8) 84)
	(= (fly-cost loc2 depot) 109)
	(= (fly-cost loc2 loc1) 59)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 125)
	(= (fly-cost loc2 loc4) 64)
	(= (fly-cost loc2 loc5) 71)
	(= (fly-cost loc2 loc6) 102)
	(= (fly-cost loc2 loc7) 122)
	(= (fly-cost loc2 loc8) 117)
	(= (fly-cost loc3 depot) 104)
	(= (fly-cost loc3 loc1) 164)
	(= (fly-cost loc3 loc2) 125)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 62)
	(= (fly-cost loc3 loc5) 156)
	(= (fly-cost loc3 loc6) 82)
	(= (fly-cost loc3 loc7) 105)
	(= (fly-cost loc3 loc8) 155)
	(= (fly-cost loc4 depot) 81)
	(= (fly-cost loc4 loc1) 109)
	(= (fly-cost loc4 loc2) 64)
	(= (fly-cost loc4 loc3) 62)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 109)
	(= (fly-cost loc4 loc6) 62)
	(= (fly-cost loc4 loc7) 101)
	(= (fly-cost loc4 loc8) 128)
	(= (fly-cost loc5 depot) 176)
	(= (fly-cost loc5 loc1) 26)
	(= (fly-cost loc5 loc2) 71)
	(= (fly-cost loc5 loc3) 156)
	(= (fly-cost loc5 loc4) 109)
	(= (fly-cost loc5 loc5) 1)
	(= (fly-cost loc5 loc6) 164)
	(= (fly-cost loc5 loc7) 97)
	(= (fly-cost loc5 loc8) 59)
	(= (fly-cost loc6 depot) 23)
	(= (fly-cost loc6 loc1) 159)
	(= (fly-cost loc6 loc2) 102)
	(= (fly-cost loc6 loc3) 82)
	(= (fly-cost loc6 loc4) 62)
	(= (fly-cost loc6 loc5) 164)
	(= (fly-cost loc6 loc6) 1)
	(= (fly-cost loc6 loc7) 160)
	(= (fly-cost loc6 loc8) 189)
	(= (fly-cost loc7 depot) 180)
	(= (fly-cost loc7 loc1) 118)
	(= (fly-cost loc7 loc2) 122)
	(= (fly-cost loc7 loc3) 105)
	(= (fly-cost loc7 loc4) 101)
	(= (fly-cost loc7 loc5) 97)
	(= (fly-cost loc7 loc6) 160)
	(= (fly-cost loc7 loc7) 1)
	(= (fly-cost loc7 loc8) 60)
	(= (fly-cost loc8 depot) 206)
	(= (fly-cost loc8 loc1) 84)
	(= (fly-cost loc8 loc2) 117)
	(= (fly-cost loc8 loc3) 155)
	(= (fly-cost loc8 loc4) 128)
	(= (fly-cost loc8 loc5) 59)
	(= (fly-cost loc8 loc6) 189)
	(= (fly-cost loc8 loc7) 60)
	(= (fly-cost loc8 loc8) 1)
)
(:goal (and
	(has-content person2 food)
	(has-content person2 medicine)
	(has-content person3 medicine)
	(has-content person4 medicine)
	(has-content person5 medicine)
	(has-content person6 medicine)
	(has-content person7 medicine)
	(has-content person8 medicine)
	))
(:metric minimize (total-cost))
)
