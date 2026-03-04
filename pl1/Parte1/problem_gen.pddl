(define (problem problem_gen)
(:domain emergency-services)
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
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	left right - arm
	food - content
	medicine - content
)
(:init
	(at-drone drone1 depot)
	(hand-empty drone1 left)
	(hand-empty drone1 right)
	(at-crate crate1 depot)
	(crate-content crate1 food)
	(at-crate crate2 depot)
	(crate-content crate2 food)
	(at-crate crate3 depot)
	(crate-content crate3 medicine)
	(at-crate crate4 depot)
	(crate-content crate4 medicine)
	(at-crate crate5 depot)
	(crate-content crate5 medicine)
	(at-crate crate6 depot)
	(crate-content crate6 medicine)
	(at-person person1 loc5)
	(at-person person2 loc4)
	(at-person person3 loc2)
	(at-person person4 loc1)
	(at-person person5 loc3)
	(at-person person6 loc4)
)
(:goal (and
	(has-content person1 medicine)
	(has-content person4 food)
	(has-content person4 medicine)
	(has-content person5 medicine)
	(has-content person6 food)
	(has-content person6 medicine)
))
)
