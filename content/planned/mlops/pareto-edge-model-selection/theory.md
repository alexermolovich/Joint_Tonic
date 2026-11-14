# Select a Pareto Model Under Accuracy and Latency Limits

## Intuition

A faster model may be less accurate. Pareto analysis keeps candidates whose tradeoffs cannot be improved on both axes at once; a deployment constraint then selects among feasible measurements.

## Dominance and a final choice

For model i with dimensionless accuracy a_i and measured milliseconds l_i,

$$i\succ j\iff a_i\ge a_j\land l_i\le l_j\land(a_i>a_j\lor l_i<l_j).$$

The frontier contains points dominated by none. Feasible points satisfy a_i>=a_min and l_i<=l_max. The deterministic selection orders by(-a_i,l_i,id_i). Identical points do not dominate each other because no inequality is strict.

## Visual: competing tradeoffs

| Model | Accuracy | Latency ms | Frontier? |
|---|---:|---:|---|
| fast | 0.8 | 2 | yes |
| accurate | 0.9 | 5 | yes |
| inferior | 0.7 | 4 | no, fast dominates |

For minimum accuracy0.75 and latency limit3ms, select fast. The table is an original scatterplot alternative.

## Why this matters on a robot

A control deadline can exclude the most accurate policy. Mixing measurements from different sensors, precision modes, or devices creates a false frontier. This task assumes comparable evidence and does not establish it.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
