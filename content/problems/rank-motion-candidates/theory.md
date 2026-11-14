# Rank Multi-Seed Motion Trajectories

## Intuition

A low objective is useful only for a candidate that meets the required gates. Filter first, then rank costs with a reproducible tie policy so the chosen seed does not depend on incidental sort behavior.

## Mathematics and conventions

For endpoint error $e_i$, tolerance $\tau$, supplied collision flag $c_i$ and limit flag $l_i$,

$$F_i=c_i\land l_i\land(e_i\le\tau).$$

Sort the indices with $F_i$ true lexicographically by objective $J_i$ and then original index i. If this set is empty, the best index is -1. Error/tolerance share normalized distance units, and all objectives use one common normalized cost; the Boolean flags are supplied evidence, not geometric calculations.

## Visual computation trace

| Candidate | Error<=0.1 | Objective | Eligible rank |
| --- | --- | --- | --- |
| 0 | yes | 3 | first |
| 1 | no | 1 | excluded |
| 2 | yes | 3 | second by original index |

## Worked examples

1. Errors `[0.1,0.2,0.05]`, both flags all True, objectives `[3.,1.,3.]`, tolerance `0.1` give feasible `[True,False,True]`, order `[0,2]`, best `0`.
2. Errors `[0.]`, collision flag `[False]`, limits flag `[True]`, objective `[0.]`, tolerance `0` give feasible `[False]`, empty int64 order and best `-1`.

## Why this matters on a robot

Choosing the smallest cost before checking feasibility can select a colliding or unreachable trajectory. Preserve the provenance of the flags: a coarse sampled validator cannot support a stronger continuous guarantee.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2310.17274). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
