(define (domain emergency-services-transporters)
  (:requirements :strips :typing)

  (:types
    location person drone crate content transporter num
  )

  (:predicates
    (at-drone ?d - drone ?l - location)
    (at-person ?p - person ?l - location)
    (at-crate ?c - crate ?l - location)
    (at-transporter ?t - transporter ?l - location)
    (hand-empty ?d - drone)
    (holding ?d - drone ?c - crate)
    (crate-content ?c - crate ?cnt - content)
    (has-content ?p - person ?cnt - content)
    (in-transporter ?c - crate ?t - transporter)
    (free-slots ?t - transporter ?n - num)
    (siguiente ?n1 - num ?n2 - num)
  )

  (:action fly
  :parameters (?d - drone ?from - location ?to - location)
  :precondition (at-drone ?d ?from)
  :effect (and
    (not (at-drone ?d ?from))
    (at-drone ?d ?to)
  )
)

  (:action pick-up
    :parameters (?d - drone ?c - crate ?l - location)
    :precondition (and
      (at-drone ?d ?l)
      (at-crate ?c ?l)
      (hand-empty ?d)
    )
    :effect (and
      (not (at-crate ?c ?l))
      (not (hand-empty ?d))
      (holding ?d ?c)
    )
  )

  (:action deliver
    :parameters (?d - drone ?c - crate ?p - person ?l - location ?cnt - content)
    :precondition (and
      (at-drone ?d ?l)
      (at-person ?p ?l)
      (holding ?d ?c)
      (crate-content ?c ?cnt)
    )
    :effect (and
      (not (holding ?d ?c))
      (hand-empty ?d)
      (has-content ?p ?cnt)
    )
  )

  (:action put-in-transporter
    :parameters (?d - drone ?c - crate ?t - transporter ?l - location ?n-new - num ?n-old - num)
    :precondition (and
      (at-drone ?d ?l)
      (at-transporter ?t ?l)
      (holding ?d ?c)
      (free-slots ?t ?n-old)
      (siguiente ?n-new ?n-old)
    )
    :effect (and
      (not (holding ?d ?c))
      (hand-empty ?d)
      (in-transporter ?c ?t)
      (not (free-slots ?t ?n-old))
      (free-slots ?t ?n-new)
    )
  )

  (:action move-transporter
    :parameters (?d - drone ?t - transporter ?from - location ?to - location)
    :precondition (and
      (at-drone ?d ?from)
      (at-transporter ?t ?from)
      (hand-empty ?d)
    )
    :effect (and
      (not (at-drone ?d ?from))
      (at-drone ?d ?to)
      (not (at-transporter ?t ?from))
      (at-transporter ?t ?to)
    )
  )

  (:action take-out-transporter
    :parameters (?d - drone ?c - crate ?t - transporter ?l - location ?n-old - num ?n-new - num)
    :precondition (and
      (at-drone ?d ?l)
      (at-transporter ?t ?l)
      (in-transporter ?c ?t)
      (hand-empty ?d)
      (free-slots ?t ?n-old)
      (siguiente ?n-old ?n-new)
    )
    :effect (and
      (not (in-transporter ?c ?t))
      (not (hand-empty ?d))
      (holding ?d ?c)
      (not (free-slots ?t ?n-old))
      (free-slots ?t ?n-new)
    )
  )
)