(define (problem problem_d1_r0_l7_p7_c7_g7)
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
    loc7 - location
    person1 - person
    person2 - person
    person3 - person
    person4 - person
    person5 - person
    person6 - person
    person7 - person
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
    crate6 - crate
    crate7 - crate
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
    (at-crate crate7 depot)
    (at-person person1 loc6)
    (at-person person2 loc5)
    (at-person person3 loc3)
    (at-person person4 loc7)
    (at-person person5 loc4)
    (at-person person6 loc3)
    (at-person person7 loc4)
    (crate-content crate1 food)
    (crate-content crate2 food)
    (crate-content crate3 food)
    (crate-content crate4 medicine)
    (crate-content crate5 medicine)
    (crate-content crate6 medicine)
    (crate-content crate7 medicine)
  )
  (:goal (and
    (has-content person2 medicine)
    (has-content person3 medicine)
    (has-content person4 food)
    (has-content person4 medicine)
    (has-content person5 food)
    (has-content person5 medicine)
    (has-content person6 food)
  ))
)
