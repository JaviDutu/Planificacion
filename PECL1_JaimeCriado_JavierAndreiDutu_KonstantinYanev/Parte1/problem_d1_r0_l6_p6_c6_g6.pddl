(define (problem problem_d1_r0_l6_p6_c6_g6)
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
    person1 - person
    person2 - person
    person3 - person
    person4 - person
    person5 - person
    person6 - person
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
    crate6 - crate
    food - content
    medicine - content
    left - arm
    right - arm
  )
  (:init
    (at-drone drone1 depot)
    (hand-empty drone1 left)
    (hand-empty drone1 right)
    (at-crate crate1 depot)
    (at-crate crate2 depot)
    (at-crate crate3 depot)
    (at-crate crate4 depot)
    (at-crate crate5 depot)
    (at-crate crate6 depot)
    (at-person person1 loc1)
    (at-person person2 loc4)
    (at-person person3 loc6)
    (at-person person4 loc1)
    (at-person person5 loc6)
    (at-person person6 loc3)
    (crate-content crate1 food)
    (crate-content crate2 food)
    (crate-content crate3 food)
    (crate-content crate4 food)
    (crate-content crate5 food)
    (crate-content crate6 medicine)
  )
  (:goal (and
    (has-content person1 food)
    (has-content person2 food)
    (has-content person3 food)
    (has-content person4 medicine)
    (has-content person5 food)
    (has-content person6 food)
  ))
)
