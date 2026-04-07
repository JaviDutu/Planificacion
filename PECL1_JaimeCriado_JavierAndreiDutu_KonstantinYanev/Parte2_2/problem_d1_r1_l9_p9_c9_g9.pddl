(define (problem problem_d1_r1_l9_p9_c9_g9)
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
	loc9 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	crate8 - crate
	crate9 - crate
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
	person9 - person
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
	(at-crate crate9 depot)
	(at-person person1 loc3)
	(at-person person2 loc5)
	(at-person person3 loc2)
	(at-person person4 loc2)
	(at-person person5 loc2)
	(at-person person6 loc5)
	(at-person person7 loc1)
	(at-person person8 loc5)
	(at-person person9 loc6)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 food)
	(crate-content crate4 food)
	(crate-content crate5 food)
	(crate-content crate6 food)
	(crate-content crate7 medicine)
	(crate-content crate8 medicine)
	(crate-content crate9 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (total-cost) 0)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 172)
	(= (fly-cost depot loc2) 211)
	(= (fly-cost depot loc3) 124)
	(= (fly-cost depot loc4) 176)
	(= (fly-cost depot loc5) 148)
	(= (fly-cost depot loc6) 183)
	(= (fly-cost depot loc7) 64)
	(= (fly-cost depot loc8) 180)
	(= (fly-cost depot loc9) 234)
	(= (fly-cost loc1 depot) 172)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 73)
	(= (fly-cost loc1 loc3) 53)
	(= (fly-cost loc1 loc4) 23)
	(= (fly-cost loc1 loc5) 119)
	(= (fly-cost loc1 loc6) 241)
	(= (fly-cost loc1 loc7) 124)
	(= (fly-cost loc1 loc8) 192)
	(= (fly-cost loc1 loc9) 175)
	(= (fly-cost loc2 depot) 211)
	(= (fly-cost loc2 loc1) 73)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 92)
	(= (fly-cost loc2 loc4) 51)
	(= (fly-cost loc2 loc5) 98)
	(= (fly-cost loc2 loc6) 219)
	(= (fly-cost loc2 loc7) 150)
	(= (fly-cost loc2 loc8) 160)
	(= (fly-cost loc2 loc9) 117)
	(= (fly-cost loc3 depot) 124)
	(= (fly-cost loc3 loc1) 53)
	(= (fly-cost loc3 loc2) 92)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 53)
	(= (fly-cost loc3 loc5) 84)
	(= (fly-cost loc3 loc6) 197)
	(= (fly-cost loc3 loc7) 72)
	(= (fly-cost loc3 loc8) 155)
	(= (fly-cost loc3 loc9) 160)
	(= (fly-cost loc4 depot) 176)
	(= (fly-cost loc4 loc1) 23)
	(= (fly-cost loc4 loc2) 51)
	(= (fly-cost loc4 loc3) 53)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 103)
	(= (fly-cost loc4 loc6) 227)
	(= (fly-cost loc4 loc7) 123)
	(= (fly-cost loc4 loc8) 175)
	(= (fly-cost loc4 loc9) 154)
	(= (fly-cost loc5 depot) 148)
	(= (fly-cost loc5 loc1) 119)
	(= (fly-cost loc5 loc2) 98)
	(= (fly-cost loc5 loc3) 84)
	(= (fly-cost loc5 loc4) 103)
	(= (fly-cost loc5 loc5) 1)
	(= (fly-cost loc5 loc6) 125)
	(= (fly-cost loc5 loc7) 86)
	(= (fly-cost loc5 loc8) 74)
	(= (fly-cost loc5 loc9) 89)
	(= (fly-cost loc6 depot) 183)
	(= (fly-cost loc6 loc1) 241)
	(= (fly-cost loc6 loc2) 219)
	(= (fly-cost loc6 loc3) 197)
	(= (fly-cost loc6 loc4) 227)
	(= (fly-cost loc6 loc5) 125)
	(= (fly-cost loc6 loc6) 1)
	(= (fly-cost loc6 loc7) 153)
	(= (fly-cost loc6 loc8) 62)
	(= (fly-cost loc6 loc9) 143)
	(= (fly-cost loc7 depot) 64)
	(= (fly-cost loc7 loc1) 124)
	(= (fly-cost loc7 loc2) 150)
	(= (fly-cost loc7 loc3) 72)
	(= (fly-cost loc7 loc4) 123)
	(= (fly-cost loc7 loc5) 86)
	(= (fly-cost loc7 loc6) 153)
	(= (fly-cost loc7 loc7) 1)
	(= (fly-cost loc7 loc8) 132)
	(= (fly-cost loc7 loc9) 174)
	(= (fly-cost loc8 depot) 180)
	(= (fly-cost loc8 loc1) 192)
	(= (fly-cost loc8 loc2) 160)
	(= (fly-cost loc8 loc3) 155)
	(= (fly-cost loc8 loc4) 175)
	(= (fly-cost loc8 loc5) 74)
	(= (fly-cost loc8 loc6) 62)
	(= (fly-cost loc8 loc7) 132)
	(= (fly-cost loc8 loc8) 1)
	(= (fly-cost loc8 loc9) 84)
	(= (fly-cost loc9 depot) 234)
	(= (fly-cost loc9 loc1) 175)
	(= (fly-cost loc9 loc2) 117)
	(= (fly-cost loc9 loc3) 160)
	(= (fly-cost loc9 loc4) 154)
	(= (fly-cost loc9 loc5) 89)
	(= (fly-cost loc9 loc6) 143)
	(= (fly-cost loc9 loc7) 174)
	(= (fly-cost loc9 loc8) 84)
	(= (fly-cost loc9 loc9) 1)
)
(:goal (and
	(has-content person1 food)
	(has-content person2 food)
	(has-content person2 medicine)
	(has-content person4 food)
	(has-content person5 food)
	(has-content person5 medicine)
	(has-content person6 food)
	(has-content person8 food)
	(has-content person9 medicine)
	))
(:metric minimize (total-cost))
)
