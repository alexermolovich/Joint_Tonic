# Build a Per-Embodiment Transfer Matrix

## Intuition

Cross-robot results form a grid, not one universal score. The training condition on one axis and evaluated robot on the other must remain visible. Missing evaluation cannot be silently turned into failure or success.

## Aggregate evidence for each cell

Let S be the number of source conditions and T the number of targets. For cell(i,j), sum supplied success and trial counts:

$$
C_{ij}=\sum_{r\in R_{ij}}s_r,\qquad N_{ij}=\sum_{r\in R_{ij}}n_r,\qquad
P_{ij}=\begin{cases}C_{ij}/N_{ij},&N_{ij}>0,\\\mathrm{NaN},&N_{ij}=0.\end{cases}
$$

$R_{ij}$ contains the records for that pair. Counts are dimensionless numbers of rollouts. The observed mask is $O_{ij}=\mathbf1[N_{ij}>0]$. Preserve caller axis order; sorting labels would change the meaning of each matrix position.

## Visual: missing is different from zero

| Training condition | arm_b | arm_a |
|---|---|---|
| mixed | unmeasured: NaN, observed=false | 0/3: rate0, observed=true |

This table is the matrix visual and text alternative. Both success counters are zero, but their denominators differ.

## Why pool counts

The first example combines1/2 and9/10. Each rollout gets one vote, so the rate is10/12. Averaging the two percentages gives equal influence to groups with different counts and answers a different question.

## Why this matters on a robot

A mixture can improve one embodiment while hurting another. Aggregate results can hide negative transfer, and missing target evaluations can look like coverage if filled with zero. Keep the matrix, task definitions, dataset versions and baseline identity together before drawing conclusions.

## Questions

1. Why are absent rates NaN rather than0?
2. Is a high off-diagonal rate alone evidence of positive transfer?

## Sources and prerequisites

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864), SectionIV data consolidation and SectionV cross-embodiment evaluation. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

