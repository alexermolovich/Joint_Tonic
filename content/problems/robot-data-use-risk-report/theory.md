# Generate a Data-Use Risk Report

## Intuition

A declared dataset use can conflict with several documented restrictions at once. Preserve every reason for review instead of producing an unexplained yes/no permission decision.

## Formal model

For dataset $i$, let $F_i$ be the set of declared mismatch predicates that evaluate true for a requested use and embodiment.
$$\operatorname{needs\_review}_i=\mathbf1[|F_i|>0].$$
Set membership checks are deterministic and dimensionless. This is an original checklist implementation; a zero count is not evidence of legal authorization or representative data.

## Worked state and shape trace

```text
Example1: request research/fr3, declared intended research, no personal data,
known license, matching embodiment -> flags=[], needs_review=False.
Example2: request commercial/panda, personal data with unknown consent,
unknown license, intended research and prohibited commercial ->
flags=["consent_unknown", "outside_intended_use", "prohibited_use",
       "unknown_license", "unsupported_embodiment"], needs_review=True.
Neither result grants legal authorization or verifies actual consent.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Robot datasets can include people, private spaces and embodiment-specific demonstrations. Documentation gaps should be visible before reuse; this exercise does not make legal conclusions.

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
