(define (problem problem_d1_r0_l2_p2_c2_g2)
  (:domain emergency-services)
  (:objects
    drone1 - drone
    depot - location
    loc1 - location
    loc2 - location
    person1 - person
    person2 - person
    crate1 - crate
    crate2 - crate
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
    (at-person person1 loc2)
    (at-person person2 loc2)
    (crate-content crate1 food)
    (crate-content crate2 medicine)
  )
  (:goal (and
    (has-content person1 food)
    (has-content person2 medicine)
  ))
)
