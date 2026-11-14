# Audit Data and Calibration Lineage

## Intuition

A calibration matrix without the session and validity interval can be the wrong calibration. Bind every episode to a declared calibration identity and report all mismatches independently.

## Formal model

For episode interval $[s_e, t_e)$ and calibration interval $[s_c, t_c)$, coverage requires
$$s_c\le s_e<t_e\le t_c.$$
Session, robot and digest identities must also agree. Timestamp values are integer nanoseconds on a shared clock; comparing integers avoids precision loss from converting large epoch values to float.

## Worked state and shape trace

```text
Calibration k: session=s, robot=r, hash=h1, valid interval [0,10) ns.
Episode b: session=other, robot=r, hash=h2, interval [9,11) ns.
Returned issues:
[("b", "digest_mismatch"), ("b", "session_mismatch"), ("b", "validity_gap")]
The intervals overlap, but the calibration does not cover the complete episode.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Distributed robot collection can reuse a camera or move a sensor between sessions. Partial temporal overlap does not establish a valid transform for the whole episode.

## Source and scope

Original bounded component inspired by [2024-droid](https://arxiv.org/abs/2403.12945). It does not reproduce the full paper or establish hardware safety or data-use authorization.
