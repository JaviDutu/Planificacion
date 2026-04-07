(define (problem problem_d1_r0_l5_p5_c5_g5)
  (:domain emergency-services)
  (:objects
    drone1 - drone
    depot - location
    loc1 - location
    loc2 - location
    loc3 - location
    loc4 - location
    loc5 - location
    person1 - person
    person2 - person
    person3 - person
    person4 - person
    person5 - person
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
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
    (at-person person1 loc1)
    (at-person person2 loc1)
    (at-person person3 loc4)
    (at-person person4 loc5)
    (at-person person5 loc5)
    (crate-content crate1 food)
    (crate-content crate2 food)
    (crate-content crate3 food)
    (crate-content crate4 medicine)
    (crate-content crate5 medicine)
  )
  (:goal (and
    (has-content person1 food)
    (has-content person2 food)
    (has-content person2 medicine)
    (has-content person3 medicine)
    (has-content person5 food)
  ))
)
