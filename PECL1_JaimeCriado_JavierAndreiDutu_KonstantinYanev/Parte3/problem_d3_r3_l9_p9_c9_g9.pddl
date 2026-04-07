(define (problem problem_d3_r3_l9_p9_c9_g9)
(:domain emergency-services-transporters)
(:objects
	drone1 - drone
	drone2 - drone
	drone3 - drone
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
	transporter2 - transporter
	transporter3 - transporter
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
	(at-transporter transporter1 depot)
	(free-slots transporter1 n4)
	(transporter-free transporter1)
	(at-transporter transporter2 depot)
	(free-slots transporter2 n4)
	(transporter-free transporter2)
	(at-transporter transporter3 depot)
	(free-slots transporter3 n4)
	(transporter-free transporter3)
	(at-crate crate1 depot)
	(at-crate crate2 depot)
	(at-crate crate3 depot)
	(at-crate crate4 depot)
	(at-crate crate5 depot)
	(at-crate crate6 depot)
	(at-crate crate7 depot)
	(at-crate crate8 depot)
	(at-crate crate9 depot)
	(at-person person1 loc9)
	(person-free person1)
	(at-person person2 loc5)
	(person-free person2)
	(at-person person3 loc8)
	(person-free person3)
	(at-person person4 loc2)
	(person-free person4)
	(at-person person5 loc7)
	(person-free person5)
	(at-person person6 loc6)
	(person-free person6)
	(at-person person7 loc4)
	(person-free person7)
	(at-person person8 loc5)
	(person-free person8)
	(at-person person9 loc3)
	(person-free person9)
	(crate-content crate1 food)
	(crate-content crate2 food)
	(crate-content crate3 food)
	(crate-content crate4 food)
	(crate-content crate5 food)
	(crate-content crate6 food)
	(crate-content crate7 food)
	(crate-content crate8 medicine)
	(crate-content crate9 medicine)
	(siguiente n0 n1)
	(siguiente n1 n2)
	(siguiente n2 n3)
	(siguiente n3 n4)
	(= (fly-cost depot depot) 1)
	(= (fly-cost depot loc1) 223)
	(= (fly-cost depot loc2) 68)
	(= (fly-cost depot loc3) 182)
	(= (fly-cost depot loc4) 131)
	(= (fly-cost depot loc5) 154)
	(= (fly-cost depot loc6) 161)
	(= (fly-cost depot loc7) 135)
	(= (fly-cost depot loc8) 82)
	(= (fly-cost depot loc9) 196)
	(= (fly-cost loc1 depot) 223)
	(= (fly-cost loc1 loc1) 1)
	(= (fly-cost loc1 loc2) 189)
	(= (fly-cost loc1 loc3) 67)
	(= (fly-cost loc1 loc4) 96)
	(= (fly-cost loc1 loc5) 74)
	(= (fly-cost loc1 loc6) 69)
	(= (fly-cost loc1 loc7) 98)
	(= (fly-cost loc1 loc8) 142)
	(= (fly-cost loc1 loc9) 84)
	(= (fly-cost loc2 depot) 68)
	(= (fly-cost loc2 loc1) 189)
	(= (fly-cost loc2 loc2) 1)
	(= (fly-cost loc2 loc3) 134)
	(= (fly-cost loc2 loc4) 94)
	(= (fly-cost loc2 loc5) 115)
	(= (fly-cost loc2 loc6) 140)
	(= (fly-cost loc2 loc7) 123)
	(= (fly-cost loc2 loc8) 70)
	(= (fly-cost loc2 loc9) 188)
	(= (fly-cost loc3 depot) 182)
	(= (fly-cost loc3 loc1) 67)
	(= (fly-cost loc3 loc2) 134)
	(= (fly-cost loc3 loc3) 1)
	(= (fly-cost loc3 loc4) 55)
	(= (fly-cost loc3 loc5) 34)
	(= (fly-cost loc3 loc6) 72)
	(= (fly-cost loc3 loc7) 90)
	(= (fly-cost loc3 loc8) 107)
	(= (fly-cost loc3 loc9) 119)
	(= (fly-cost loc4 depot) 131)
	(= (fly-cost loc4 loc1) 96)
	(= (fly-cost loc4 loc2) 94)
	(= (fly-cost loc4 loc3) 55)
	(= (fly-cost loc4 loc4) 1)
	(= (fly-cost loc4 loc5) 24)
	(= (fly-cost loc4 loc6) 51)
	(= (fly-cost loc4 loc7) 50)
	(= (fly-cost loc4 loc8) 53)
	(= (fly-cost loc4 loc9) 105)
	(= (fly-cost loc5 depot) 154)
	(= (fly-cost loc5 loc1) 74)
	(= (fly-cost loc5 loc2) 115)
	(= (fly-cost loc5 loc3) 34)
	(= (fly-cost loc5 loc4) 24)
	(= (fly-cost loc5 loc5) 1)
	(= (fly-cost loc5 loc6) 46)
	(= (fly-cost loc5 loc7) 57)
	(= (fly-cost loc5 loc8) 76)
	(= (fly-cost loc5 loc9) 98)
	(= (fly-cost loc6 depot) 161)
	(= (fly-cost loc6 loc1) 69)
	(= (fly-cost loc6 loc2) 140)
	(= (fly-cost loc6 loc3) 72)
	(= (fly-cost loc6 loc4) 51)
	(= (fly-cost loc6 loc5) 46)
	(= (fly-cost loc6 loc6) 1)
	(= (fly-cost loc6 loc7) 29)
	(= (fly-cost loc6 loc8) 80)
	(= (fly-cost loc6 loc9) 54)
	(= (fly-cost loc7 depot) 135)
	(= (fly-cost loc7 loc1) 98)
	(= (fly-cost loc7 loc2) 123)
	(= (fly-cost loc7 loc3) 90)
	(= (fly-cost loc7 loc4) 50)
	(= (fly-cost loc7 loc5) 57)
	(= (fly-cost loc7 loc6) 29)
	(= (fly-cost loc7 loc7) 1)
	(= (fly-cost loc7 loc8) 58)
	(= (fly-cost loc7 loc9) 65)
	(= (fly-cost loc8 depot) 82)
	(= (fly-cost loc8 loc1) 142)
	(= (fly-cost loc8 loc2) 70)
	(= (fly-cost loc8 loc3) 107)
	(= (fly-cost loc8 loc4) 53)
	(= (fly-cost loc8 loc5) 76)
	(= (fly-cost loc8 loc6) 80)
	(= (fly-cost loc8 loc7) 58)
	(= (fly-cost loc8 loc8) 1)
	(= (fly-cost loc8 loc9) 122)
	(= (fly-cost loc9 depot) 196)
	(= (fly-cost loc9 loc1) 84)
	(= (fly-cost loc9 loc2) 188)
	(= (fly-cost loc9 loc3) 119)
	(= (fly-cost loc9 loc4) 105)
	(= (fly-cost loc9 loc5) 98)
	(= (fly-cost loc9 loc6) 54)
	(= (fly-cost loc9 loc7) 65)
	(= (fly-cost loc9 loc8) 122)
	(= (fly-cost loc9 loc9) 1)
)
(:goal (and
	(has-content person1 food)
	(has-content person2 food)
	(has-content person2 medicine)
	(has-content person4 food)
	(has-content person5 food)
	(has-content person6 food)
	(has-content person6 medicine)
	(has-content person8 food)
	(has-content person9 food)
	))
(:metric minimize (total-time))
)
