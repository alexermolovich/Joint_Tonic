# Choose a Collision-Free Minimum-Cost Tree Parent

## Intuition

A nearby vertex is not necessarily a cheap parent, and a cheap connection is useless if its path collides. Selection must combine accumulated root cost with the cost of the new edge while excluding infeasible candidates.

## Mathematics and conventions

Let $c_i\ge0$ be cost from the root to candidate $i$, $e_i\ge0$ the connecting-edge cost, and $F_i$ its supplied feasibility flag:

$$i^*=\operatorname*{argmin}_{i:F_i}(c_i+e_i).$$

All costs share one unit; $F$ is dimensionless Boolean evidence. Exact cost ties choose the smallest original index. If the feasible set is empty, the output is the explicit pair $(-1,+\infty)$, not an arbitrary root vertex.

## Visual computation trace

| Candidate | Root cost | Edge cost | Total |
| --- | --- | --- | --- |
| 0 | 3 | 1 | 4 |
| 1 | 1 | 4 | 5 |
| 2 | 2 | 2 | 4 |

## Worked examples

1. Root costs `[3.,1.,2.]`, edge costs `[1.,4.,2.]`, all feasible gives totals `[4.,5.,4.]`: parent0 and total_cost4, using the lower index for a tie.
2. Root costs `[0.,5.]`, edge costs `[0.,1.]`, feasible `[False,False]` returns parent -1 and total_cost +infinity. An infeasible cheap connection cannot become a parent.

## Why this matters on a robot

Ignoring accumulated root cost makes the planner greedily prefer short local edges without improving the complete route. A missing feasible parent must prevent insertion; treating index -1 as a Python array index would accidentally select the last candidate.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1005.0416). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
