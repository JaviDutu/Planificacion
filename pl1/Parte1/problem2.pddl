(define (problem problem2)
  (:domain emergency-services)
  (:objects
    d1 - drone
    depot loc1 loc2 - location
    p1 p2 - person
    c1 c2 c3 - crate
    food medicine - content
    left right - arm
  )
  (:init
    (at-drone d1 depot)
    (at-crate c1 depot)
    (at-crate c2 depot)
    (at-crate c3 depot)
    (at-person p1 loc1)
    (at-person p2 loc2)
    (crate-content c1 food)
    (crate-content c2 medicine)
    (crate-content c3 food)
    (hand-empty d1 left)
    (hand-empty d1 right)
  )
  (:goal
    (and
      (has-content p1 food)
      (has-content p2 medicine)
    )
  )
)