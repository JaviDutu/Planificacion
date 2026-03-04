(define (problem problem1)
  (:domain emergency-services)
  (:objects
    d1 - drone
    depot loc1 - location
    p1 - person
    c1 - crate
    food - content
    left right - arm
  )
  (:init
    (at-drone d1 depot)
    (at-crate c1 depot)
    (at-person p1 loc1)
    (crate-content c1 food)
    (hand-empty d1 left)
    (hand-empty d1 right)
  )
  (:goal
    (has-content p1 food)
  )
)