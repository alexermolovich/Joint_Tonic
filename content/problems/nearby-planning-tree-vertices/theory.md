# Find Nearby Planning Tree Vertices

## Intuition

Tree expansion needs a well-defined neighborhood before it can choose or rewire a parent. Explicit feature weights prevent one coordinate scale from silently dominating proximity.

## Mathematics and conventions

For normalized vertex $v_i\in\mathbb R^D$, query $q$, positive dimensionless metric weights $w$, and radius $r$,

$$d_i^2=\sum_jw_j(v_{ij}-q_j)^2,\qquad \mathcal N=\{i:d_i^2\le r^2\}.$$

Comparing squared distances avoids a square root in the membership test. Returned distances are $\sqrt{d_i^2}$. The metric is Euclidean after coordinate scaling by $\sqrt w$; periodic joints require a different declared difference rule.

## Visual computation trace

| Vertex | Weighted squared distance | Included at radius2? |
| --- | --- | --- |
| (0,0) | 0 | yes |
| (1,0) | 4 | yes |
| (0,2) | 4 | yes |

## Worked examples

1. Vertices `[[0.,0.],[1.,0.],[0.,2.]]`, query `[0.,0.]`, weights `[4.,1.]`, radius2 gives indices `[0,1,2]` and distances `[0.,2.,2.]`; boundary vertices are included.
2. Vertices `[[1.],[0.],[0.]]`, query `[0.]`, weight `[1.]`, radius0 gives indices `[1,2]`, distances `[0.,0.]`, preserving duplicates and index order.

## Why this matters on a robot

Treating angles near minus-pi and plus-pi as far apart can distort a planner, but silently wrapping every feature is equally wrong for bounded joints. This component deliberately uses a normalized nonperiodic metric.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1005.0416). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
