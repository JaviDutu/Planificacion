(define (problem problem_d1_r0_l10_p10_c10_g10)
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
    loc8 - location
    loc9 - location
    loc10 - location
    person1 - person
    person2 - person
    person3 - person
    person4 - person
    person5 - person
    person6 - person
    person7 - person
    person8 - person
    person9 - person
    person10 - person
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
    crate6 - crate
    crate7 - crate
    crate8 - crate
    crate9 - crate
    crate10 - crate
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
    (at-crate crate8 depot)
    (at-crate crate9 depot)
    (at-crate crate10 depot)
    (at-person person1 loc2)
    (at-person person2 loc9)
    (at-person person3 loc10)
    (at-person person4 loc8)
    (at-person person5 loc1)
    (at-person person6 loc3)
    (at-person person7 loc4)
    (at-person person8 loc10)
    (at-person person9 loc9)
    (at-person person10 loc4)
    (crate-content crate1 food)
    (crate-content crate2 food)
    (crate-content crate3 food)
    (crate-content crate4 food)
    (crate-content crate5 food)
    (crate-content crate6 food)
    (crate-content crate7 food)
    (crate-content crate8 food)
    (crate-content crate9 medicine)
    (crate-content crate10 medicine)
  )
  (:goal (and
    (has-content person1 food)
    (has-content person2 food)
    (has-content person3 food)
    (has-content person4 food)
    (has-content person4 medicine)
    (has-content person5 food)
    (has-content person6 food)
    (has-content person6 medicine)
    (has-content person7 food)
    (has-content person10 food)
  ))
)
