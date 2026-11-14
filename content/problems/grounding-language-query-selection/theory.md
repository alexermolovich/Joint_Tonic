# Select Language-Guided Object Queries

## Intuition

A visual location becomes a promising object query when it strongly matches at least one meaningful word. Padding must never compete, and equal scores need a repeatable ordering.

## Math and selection trace

Let $S\in\mathbb R^{Q\times T}$ contain visual/text compatibility and $m_t$ indicate usable text. Query score is
$$r_q=\max_{t:m_t=1}S_{qt},\qquad I=\operatorname{argsort}_q(-r_q,q)[:k].$$
All scores are dimensionless. Lexicographic sorting uses original query index for exact ties. A maximum over an empty usable set is undefined, so positive-k requests reject it. k=0 needs no ranking.

| Query | Usable scores | Maximum | Rank |
|---|---|---|---|
| 0 | 1,3 | 3 | third |
| 1 | 4,2 | 4 | first |
| 2 | 4,1 | 4 | second by index |

The unused score 100 in query 0 is removed before reduction. Replacing masked scores with zero would be wrong if every usable score is negative; boolean selection avoids that issue.

## Why this matters on a robot

Language-guided selection focuses detector capacity on instruction-relevant evidence. Mask errors can select padding rather than the intended object, while unstable ties make repeated runs harder to debug. This component selects query indices; it does not establish phrase correctness or graspability.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
