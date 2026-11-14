# Validate a Model Card Schema

## Intuition

A model card binds what was evaluated to the complete serving pipeline. Missing slice denominators and missing runtime identities are different reporting failures and should not become fabricated performance estimates.

## Formal model

For measured slice $s$ with trials $n_s$ and successes $k_s$, valid rate evidence requires
$$0\le k_s\le n_s,\qquad n_s>0.$$
The exercise verifies this evidence contract and the presence of requested slices. It deliberately does not require any minimum $k_s/n_s$. Hash identities bind weights, preprocessing, action decoding and runtime as one documented release tuple, not proof of artifact contents.

## Worked state and shape trace

```text
Required slices: day, night.
Measured: night with trials=0 and successes=1.
Returned issues:
[("day", "missing"), ("night", "invalid_success_count"), ("night", "no_trials")]
A valid day row with trials=10, successes=2 yields [] when day is the only
required slice: poor success rate alone is not a schema violation.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

A policy’s reported score is difficult to reproduce if its action decoder or runtime is unspecified. A complete card can still describe poor performance; completeness must not masquerade as approval.

## Source and scope

Original bounded component inspired by [2018-model-cards](https://arxiv.org/abs/1810.03993). It does not reproduce the full paper or establish hardware safety or data-use authorization.
