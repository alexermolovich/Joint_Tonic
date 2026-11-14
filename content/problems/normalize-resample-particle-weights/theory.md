# Normalize and Resample Particle Weights

## Intuition

A few particles may explain a sensor observation much better than the rest. Resampling allocates copies in proportion to weight. One shared offset spreads sampling positions evenly, reducing the extra randomness of independent draws.

## Mathematics and physical meaning

For nonnegative weights $w_i$ with maximum $s>0$, define $p_i=(w_i/s)/\sum_j(w_j/s)$ and cumulative mass $C_i=\sum_{j=0}^i p_j$. For user-supplied $u\in[0,1)$, systematic positions are
$$v_k=\frac{u+k}{N},\qquad a_k=\min\{i:C_i>v_k\},\quad k=0,\ldots,N-1.$$
The ancestry vector $a$ indexes the original particles. All quantities are dimensionless. Passing a recorded offset makes the exercise reproducible independently of global random state.

## Visual trace

| k | Position with N=4,u=0.5 | Cumulative [0.25,0.25,0.75,1] selects |
|---|---|---|
| 0 | 0.125 | 0 |
| 1 | 0.375 | 2 |
| 2 | 0.625 | 2 |
| 3 | 0.875 | 3 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `weights=[1,0,2,1], offset=0.5` → normalized `[0.25,0,0.5,0.25]`, ancestry `[0,2,2,3]`.
2. `weights=[0,5], offset=0` → normalized `[0,1]`, ancestry `[1,1]`; a position of zero skips zero mass.

## Why this matters on a robot

Resampling can eliminate low-weight hypotheses, so incorrect zero-weight boundary handling can revive impossible poses. This component returns ancestry only; a full particle filter still needs motion, observation likelihoods, and diversity management.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.

Numerical endpoint convention: clamp computed systematic positions to np.nextafter(1.0,0.0), because floating arithmetic can round a nominally subunit position to 1. This keeps ancestry indices in range.
