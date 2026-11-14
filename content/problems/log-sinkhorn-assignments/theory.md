# Normalize Assignments with Sinkhorn Iterations

## Intuition

Independent row softmax lets every source spend its full confidence on the same target. Transport instead asks the assignment to respect both source and target mass budgets. Alternating updates approach both constraints.

## Mathematics and conventions

Let $S\in\mathbb R^{N\times M}$ contain dimensionless log scores, $a\in\mathbb R^N$ positive row masses and $b\in\mathbb R^M$ positive column masses, each normalized to total 1. Initialize $u=0,v=0$ and repeat

$$u_i=\log a_i-\operatorname{LSE}_j(S_{ij}+v_j),\qquad v_j=\log b_j-\operatorname{LSE}_i(S_{ij}+u_i).$$

Here $\operatorname{LSE}(z)=m+\log\sum_k e^{z_k-m}$ with $m=\max_k z_k$, avoiding unstable exponentiation of the largest logit. The resulting transport is

$$P_{ij}=\exp(S_{ij}+u_i+v_j).$$

P carries dimensionless mass. Each column update may disturb the preceding row constraint. Reporting both maximum absolute marginal errors exposes incomplete convergence, particularly for sharply concentrated logits and mismatched mass budgets.

## Visual computation trace

| Budget | Row0 | Row1 | Column totals |
| --- | --- | --- | --- |
| Requested row mass | .75 | .25 | total1 |
| Column0 allocation | .375 | .125 | .5 |
| Column1 allocation | .375 | .125 | .5 |

## Worked examples

1. Zero `2x2` logits with row/column masses `[0.5,0.5]` give transport `[[0.25,0.25],[0.25,0.25]]` after one iteration.
2. Zero `2x2` logits with row masses `[0.75,0.25]` and column masses `[0.5,0.5]` give `[[0.375,0.375],[0.125,0.125]]`. Its logarithm is returned separately.

## Why this matters on a robot

Repeated visual patterns can generate highly peaked but incompatible similarities. A fixed small iteration budget may leave appreciable row error; interpreting such a matrix as a fully balanced assignment hides that failure.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1911.11763). [feature-matching-score-matrix](/problems/feature-matching-score-matrix)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
