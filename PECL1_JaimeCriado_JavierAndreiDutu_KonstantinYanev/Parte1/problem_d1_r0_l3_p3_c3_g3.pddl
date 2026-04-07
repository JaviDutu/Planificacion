(define (problem problem_d1_r0_l3_p3_c3_g3)
  (:domain emergency-services)
  (:objects
    drone1 - drone
    depot - location
    loc1 - location
    loc2 - location
    loc3 - location
    person1 - person
    person2 - person
    person3 - person
    crate1 - crate
    crate2 - crate
    crate3 - crate
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
    (at-person person1 loc2)
    (at-person person2 loc2)
    (at-person person3 loc2)
    (crate-content crate1 food)
    (crate-content crate2 medicine)
    (crate-content crate3 medicine)
  )
  (:goal (and
    (has-content person1 food)
    (has-content person2 medicine)
    (has-content person3 medicine)
  ))
)
