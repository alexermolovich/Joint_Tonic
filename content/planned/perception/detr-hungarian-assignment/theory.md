# Find a globally consistent query assignment

## Intuition

Independent best-query choices can assign the same prediction to several objects. Greedily reserving each target's favorite query can also block a much better joint solution. Assignment optimizes the whole one-to-one matching.

## The constrained objective

Let $C\in\mathbb R^{Q\times M}$ hold dimensionless query-to-target costs, Q at least M. Seek an injective map $\sigma:\{0,\ldots,M-1\}\to\{0,\ldots,Q-1\}$ minimizing

$$
\sum_{j=0}^{M-1}C_{\sigma(j),j}.
$$

Injective means two targets cannot use the same query. The returned array is indexed by target j, not sorted by query. Unmatched queries later receive no-object supervision.

## Visual: a greedy trap

| Query | Target0 cost | Target1 cost |
|---|---:|---:|
| 0 | 1 | 2 |
| 1 | 2 | 100 |

Selecting the smallest entry first costs1+100=101. Swapping both assignments costs2+2=4. The table is a static bipartite-edge-cost diagram and text alternative.

## Potentials and augmenting paths

A Hungarian-style algorithm maintains row and column potentials so reduced costs remain nonnegative. Transpose the conceptual problem to M target rows and Q query columns. For target potential $u_j$ and query potential $v_i$,

$$
r_{ji}=C_{ij}-u_j-v_i\ge0.
$$

For this rectangular assignment, each target is used exactly once while each query is used at most once. Its dual additionally requires $v_i\le0$; target potentials $u_j$ are unrestricted. The dual lower bound is $\sum_j u_j+\sum_i v_i$. An unused query must have $v_i=0$ at a complementary optimal solution.

Zero reduced-cost edges form candidates for an augmenting path. If no free query is reachable, shift potentials by the smallest unreached slack to expose another zero edge. Augmenting a path reassigns earlier targets when necessary instead of freezing greedy choices.

At completion, selected zero-reduced-cost edges, dual-feasible potentials and zero potentials on unused queries certify optimality: the assignment cost equals the dual lower bound. No permutation enumeration is needed; a rectangular implementation takes O(M²Q) time.

## Ties and evaluation

Several distinct assignments may attain the same minimum. The grader checks objective value, distinct indices and coverage, not a particular arbitrary tie order. Negative costs are valid; they do not change the assignment constraints.

## Why this matters on a robot

Set-prediction detectors need consistent supervision when objects overlap or look alike. A wrong assignment can train two queries toward one object and leave another unexplained. Correct matching alone does not guarantee good predictions; costs and the later loss remain separate.

Source: [DETR matching objective](https://arxiv.org/abs/2005.12872). Start with [cost construction](/problems/detr-matching-cost), then build [no-object targets](/problems/detr-no-object-targets). The exercise implements assignment, not a detector.
