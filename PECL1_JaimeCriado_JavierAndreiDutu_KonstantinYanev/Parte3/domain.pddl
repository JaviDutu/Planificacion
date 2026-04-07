(define (domain emergency-services-transporters)
  (:requirements :strips :typing :durative-actions :fluents)

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

    (drone-free ?d - drone)
    (transporter-free ?t - transporter)
    (person-free ?p - person)
  )

  (:functions
    (fly-cost ?from - location ?to - location)
  )


  (:durative-action fly
    :parameters (?d - drone ?from - location ?to - location)
    :duration (= ?duration (fly-cost ?from ?to))
    :condition (and
      (at start (at-drone ?d ?from))
      (at start (drone-free ?d))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (at-drone ?d ?from)))
      (at end (at-drone ?d ?to))
      (at end (drone-free ?d))
    )
  )


  (:durative-action pick-up
    :parameters (?d - drone ?c - crate ?l - location)
    :duration (= ?duration 5)
    :condition (and
      (at start (at-drone ?d ?l))
      (at start (at-crate ?c ?l))
      (at start (hand-empty ?d))
      (at start (drone-free ?d))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (at-crate ?c ?l)))
      (at start (not (hand-empty ?d)))
      (at end (holding ?d ?c))
      (at end (drone-free ?d))
    )
  )


  (:durative-action deliver
    :parameters (?d - drone ?c - crate ?p - person ?l - location ?cnt - content)
    :duration (= ?duration 5)
    :condition (and
      (at start (at-drone ?d ?l))
      (at start (at-person ?p ?l))
      (at start (holding ?d ?c))
      (at start (crate-content ?c ?cnt))
      (at start (drone-free ?d))
      (at start (person-free ?p))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (person-free ?p)))

      (at end (not (holding ?d ?c)))
      (at end (hand-empty ?d))
      (at end (has-content ?p ?cnt))

      (at end (drone-free ?d))
      (at end (person-free ?p))
    )
  )


  (:durative-action put-in-transporter
    :parameters (?d - drone ?c - crate ?t - transporter ?l - location ?n-new - num ?n-old - num)
    :duration (= ?duration 5)
    :condition (and
      (at start (at-drone ?d ?l))
      (at start (at-transporter ?t ?l))
      (at start (holding ?d ?c))
      (at start (free-slots ?t ?n-old))
      (at start (siguiente ?n-new ?n-old))
      (at start (drone-free ?d))
      (at start (transporter-free ?t))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (transporter-free ?t)))

      (at end (not (holding ?d ?c)))
      (at end (hand-empty ?d))
      (at end (in-transporter ?c ?t))

      (at end (not (free-slots ?t ?n-old)))
      (at end (free-slots ?t ?n-new))

      (at end (drone-free ?d))
      (at end (transporter-free ?t))
    )
  )


  (:durative-action move-transporter
    :parameters (?d - drone ?t - transporter ?from - location ?to - location)
    :duration (= ?duration (fly-cost ?from ?to))
    :condition (and
      (at start (at-drone ?d ?from))
      (at start (at-transporter ?t ?from))
      (at start (hand-empty ?d))
      (at start (drone-free ?d))
      (at start (transporter-free ?t))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (transporter-free ?t)))

      (at start (not (at-drone ?d ?from)))
      (at start (not (at-transporter ?t ?from)))

      (at end (at-drone ?d ?to))
      (at end (at-transporter ?t ?to))

      (at end (drone-free ?d))
      (at end (transporter-free ?t))
    )
  )


  (:durative-action take-out-transporter
    :parameters (?d - drone ?c - crate ?t - transporter ?l - location ?n-old - num ?n-new - num)
    :duration (= ?duration 5)
    :condition (and
      (at start (at-drone ?d ?l))
      (at start (at-transporter ?t ?l))
      (at start (in-transporter ?c ?t))
      (at start (hand-empty ?d))
      (at start (free-slots ?t ?n-old))
      (at start (siguiente ?n-old ?n-new))
      (at start (drone-free ?d))
      (at start (transporter-free ?t))
    )
    :effect (and
      (at start (not (drone-free ?d)))
      (at start (not (transporter-free ?t)))
      (at start (not (hand-empty ?d)))
      (at start (not (in-transporter ?c ?t)))

      (at end (holding ?d ?c))

      (at end (not (free-slots ?t ?n-old)))
      (at end (free-slots ?t ?n-new))

      (at end (drone-free ?d))
      (at end (transporter-free ?t))
    )
  )
)