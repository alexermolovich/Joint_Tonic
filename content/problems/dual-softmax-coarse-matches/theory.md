# Construct Coarse Correspondence Candidates

## Intuition

A plausible pair should compete successfully against alternatives in both images. Multiplying row and column probabilities captures those two competitions before selecting mutual matches.

## Mathematics and conventions

For dimensionless descriptors $a_i,b_j\in\mathbb R^D$ and positive temperature tau, define

$$S_{ij}=\frac{a_i^\top b_j}{D\tau},\quad R_{ij}=\frac{e^{S_{ij}}}{\sum_{k\in B}e^{S_{ik}}},\quad C_{ij}=\frac{e^{S_{ij}}}{\sum_{k\in A}e^{S_{kj}}},\quad P_{ij}=R_{ij}C_{ij}.$$

A and B here index valid source and target features. Use max-subtracted exponentials along each normalization axis; unsupported pairs have confidence zero. Unlike a single softmax, the confidence matrix need not sum to one by row or column. A retained pair is reciprocal under first-index row/column maxima of P and satisfies $P_{ij}>\eta$, where eta is the confidence threshold.

## Visual computation trace

| Two sources, one valid target | Row softmax | Column softmax | Product |
| --- | --- | --- | --- |
| Source0 to target0 | 1 | .5 | .5 |
| Source1 to target0 | 1 | .5 | .5 |
| Mutual first tie | source0 wins target choice | | pair(0,0) |

## Worked examples

1. Two zero source descriptors and two zero target descriptors, D=1, all valid, temperature 1: every confidence is 0.25. At threshold 0, first-index mutual ties retain only `[[0,0]]`; at threshold 0.25 no match survives.
2. Mask the second target in that example: the first column confidence is `[0.5,0.5]` and the second column zero. Only `[[0,0]]` survives at threshold 0.

## Why this matters on a robot

Applying the mask after an unmasked softmax lets padded descriptors steal probability mass. This changes confidence even when the padded pair is later removed, making image padding influence matching.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2104.00680). [feature-matching-score-matrix](/problems/feature-matching-score-matrix) · [extract-mutual-feature-matches](/problems/extract-mutual-feature-matches)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
