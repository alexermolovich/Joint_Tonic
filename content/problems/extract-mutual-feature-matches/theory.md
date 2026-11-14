# Extract Mutual Matches and Unmatched Labels from Transport Scores

## Intuition

Nearest-neighbor choices need not agree. Requiring a source and target to choose each other prevents many sources from claiming the same target, while a confidence threshold removes weak reciprocal coincidences.

## Mathematics and conventions

Let A be the supplied assignment including bins. Restrict attention to its real $N\times M$ block. Define first-index argmax choices

$$j_i=\operatorname{argmax}_{j<M}A_{ij},\qquad i_j=\operatorname{argmax}_{i<N}A_{ij}.$$

A source i produces a retained pair when

$$i_{j_i}=i\quad\text{and}\quad A_{i,j_i}>\tau.$$

The threshold and assignment scores are dimensionless. The output labels map original source/target indices, not ranks after sorting. Confidence is copied only for retained pairs; unmatched labels are -1 and confidences zero. Because argmax choices are single-valued even under ties, each retained source and target appears in at most one pair.

## Visual computation trace

| Real matrix | Row choices | Column choices | Retained pairs |
| --- | --- | --- | --- |
| [[.8,.1],[.2,.7]] | [0,1] | [0,1] | (0,0),(1,1) at threshold .5 |
| [[1,1],[1,1]] | [0,0] | [0,0] | (0,0) at threshold0 |

## Worked examples

1. Assignment `[[0.8,0.1,0.],[0.2,0.7,0.],[0.,0.,0.]]`, threshold 0.5: pairs `[[0,0],[1,1]]`, source and target matches `[0,1]`, confidence `[0.8,0.7]`.
2. An all-ones real `2x2` block with threshold 0 has only pair `[[0,0]]`: first-index argmax ties must be reciprocal. With threshold 1 no pair passes the strict comparison.

## Why this matters on a robot

Repeated scene structure may produce reciprocal but wrong correspondences. A very high dustbin score also remains separate from this explicit real-block extraction policy; applying an undocumented bin gate changes the task.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1911.11763). [dustbin-partial-assignment](/problems/dustbin-partial-assignment)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
