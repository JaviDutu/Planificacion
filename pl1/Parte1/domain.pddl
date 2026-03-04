(define (domain emergency-services)
  (:requirements :strips :typing)
  (:types 
    location person drone crate content arm
  )

  (:predicates
    (at-drone ?d - drone ?l - location)
    (at-person ?p - person ?l - location)
    (at-crate ?c - crate ?l - location)
    (hand-empty ?d - drone ?a - arm)
    (holding ?d - drone ?a - arm ?c - crate)
    (crate-content ?c - crate ?cnt - content)
    (has-content ?p - person ?cnt - content)
  )

  (:action fly
    :parameters (?d - drone ?from - location ?to - location)
    :precondition (at-drone ?d ?from)
    :effect (and (not (at-drone ?d ?from)) (at-drone ?d ?to))
  )

  (:action pick-up
    :parameters (?d - drone ?a - arm ?c - crate ?l - location)
    :precondition (and (at-drone ?d ?l) (at-crate ?c ?l) (hand-empty ?d ?a))
    :effect (and (not (at-crate ?c ?l)) (not (hand-empty ?d ?a)) (holding ?d ?a ?c))
  )

  (:action deliver
    :parameters (?d - drone ?a - arm ?c - crate ?p - person ?l - location ?cnt - content)
    :precondition (and (at-drone ?d ?l) (at-person ?p ?l) (holding ?d ?a ?c) (crate-content ?c ?cnt))
    :effect (and (not (holding ?d ?a ?c)) (hand-empty ?d ?a) (has-content ?p ?cnt))
  )
)