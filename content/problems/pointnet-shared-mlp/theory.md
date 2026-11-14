# Build a Shared Point MLP and Global Feature

## Intuition

Every point passes through exactly the same feature detector. A channel then records the strongest response anywhere in the cloud, so changing the order of points cannot change the global descriptor.

## Math and shape trace

Let $X\in\mathbb R^{N\times D}$ contain normalized dimensionless features, $W\in\mathbb R^{D\times F}$ shared weights and $b\in\mathbb R^F$ a shared bias. For point $i$ and output channel $j$,
$$H_{ij}=\max(0,\sum_{k=1}^{D}X_{ik}W_{kj}+b_j),\qquad g_j=\max_{1\le i\le N}H_{ij}.$$

| Stage | Shape | Meaning |
|---|---|---|
| Point features | N × D | One row per point |
| Shared affine layer | N × F | Identical detector weights on each row |
| ReLU | N × F | Negative detector evidence clipped |
| Max over rows | F | Strongest response per channel |

For $X=[[1,2],[-1,3]],W=I_2,b=[0,-2]$, the affine output is $[[1,0],[-1,1]]$, ReLU gives $[[1,0],[0,1]]$, and $g=[1,1]$. If rows are permuted by $P$, then $H(PX)=PH(X)$, while max over rows removes that permutation. This is permutation invariance, not rotation invariance.

## Why this matters on a robot

Depth sensors do not promise a stable point ordering. Sharing weights avoids making the feature extractor depend on ordering. Pooling over channels instead of points destroys this property; using unnormalized meters in a model trained on normalized coordinates changes its inputs even though the code still runs.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1612.00593). [pointnet-symmetric-pooling](/problems/pointnet-symmetric-pooling)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
