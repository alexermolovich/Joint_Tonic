# Associate Scan Points with Local Map Planes

## Intuition

Nearby points define a useful plane only when they span two directions and have a distinct least-variance normal. Keep association identity and reject unsupported geometry instead of returning an arbitrary eigenvector as reliable evidence.

## Mathematics and conventions

For K selected neighbors $p_j\in\mathbb R^3$, compute

$$\mu=K^{-1}\sum_jp_j,\qquad C=K^{-1}\sum_j(p_j-\mu)(p_j-\mu)^T.$$

The smallest-eigenvalue unit eigenvector n minimizes the sum of squared orthogonal distances. Its plane is

$$n^Tx+d=0,\qquad d=-n^T\mu.$$

Centroids and d are meters; C and its eigenvalues are square meters. The contract's radius, second-eigenvalue, eigen-gap and maximum-distance tests distinguish a supported plane from a line, an isotropic cloud or remote neighbors. Normal sign is an explicit representation convention, not a physical surface orientation.

## Visual computation trace

| Geometry | Covariance pattern | Decision |
| --- | --- | --- |
| Square in z=0 | diag(1,1,0) | normal +z, valid |
| Straight x-axis line | two zero eigenvalues | reject unsupported plane |
| Isotropic cloud | equal eigenvalues | reject ambiguous normal |

## Worked examples

1. Map corners `[[-1.,-1.,0.],[-1.,1.,0.],[1.,-1.,0.],[1.,1.,0.]]`, query `[[0.,0.,1.]]`, K=4, radius 2, tolerance 0 yield centroid `[[0.,0.,0.]]`, normal `[[0.,0.,1.]]`, offset `[0.]`, valid `[True]`. Equal-distance neighbor indices follow `[0,1,2,3]`.
2. Map points on one straight line, such as `[[0.,0.,0.],[1.,0.,0.],[2.,0.,0.]]`, have zero second eigenvalue. The fit is invalid and normal/offset are NaN, even if every neighbor is within radius.

## Why this matters on a robot

Hallways and large planes can constrain only some pose directions. A fitted plane is one measurement candidate, and its validity flag does not assess full pose observability or map staleness.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2107.06829). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
