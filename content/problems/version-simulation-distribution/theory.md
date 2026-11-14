# Version a Simulation Scenario Distribution

## Intuition

A seed cannot reproduce a simulation when the parameter bounds, reset boundary, or robot asset changed. Bind these declarations into one stable identity before comparing experiments.

## Distribution and identity

For each named factor j with declared unit u_j, endpoints l_j and h_j define an independent episode-level draw

$$\xi_j\sim\mathcal U(l_j,h_j),\qquad p(\xi)=\prod_j p_j(\xi_j).$$

A degenerate interval fixes its factor. Let N(c) sort factor records and canonicalize numbers in configuration c. Let J be the specified UTF-8 canonical JSON serialization; identity is

$$d=\operatorname{SHA256}(J(N(c))).$$

The digest is an identifier, not a numerical measure of how different two distributions are. Normalizing 1 and1.0, and signed zero, prevents irrelevant serialization changes.

## Visual normalization trace

| Supplied factor order | Normalized order | Meaning |
|---|---|---|
| yaw:rad[-0.0,1], mass:kg[1,2] | mass:kg[1.0,2.0], yaw:rad[0.0,1.0] | independent episode draws |

The table is the static visual and text alternative. Reversing supplied factor order leaves the digest unchanged; changing mass.high from2 to3 changes the canonical payload.

## Why this matters on a robot

The same numerical interval with kilograms versus a scale ratio has different physical meaning. A matching digest cannot verify that the simulator honored a declaration or that hardware lies inside the distribution. Store sampled parameters and runtime evidence alongside it.

Prerequisite: [Build a Seeded Visual Randomization Sampler](/problems/seeded-visual-randomization).

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
