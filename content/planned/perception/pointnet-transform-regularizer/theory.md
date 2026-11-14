# Keep a learned feature transform near orthogonal

## Intuition

A learned feature transform can align a point cloud's internal representation, but unrestricted scaling can distort it. An orthogonality penalty discourages that distortion while leaving the transform trainable. It is a soft preference, not a geometric constraint solver.

## Define the batch objective

Let $A_b\in\mathbb R^{D\times D}$ be the dimensionless feature transform for cloud b, and let $I_D$ be the identity. With B clouds,

$$
\mathcal L=\frac1B\sum_{b=1}^{B}
\|A_bA_b^\top-I_D\|_F^2
=\frac1B\sum_b\sum_{i,j}
\left((A_bA_b^\top)_{ij}-\delta_{ij}\right)^2.
$$

The Kronecker symbol $\delta_{ij}$ is one on the diagonal and zero otherwise. Average over clouds only. Dividing by D² would define a different regularization strength.

## Visual: scaling produces a residual

| Matrix | Diagonal entries for A=diag(2,1) |
|---|---|
| A | [2,1] |
| A Aᵀ | [4,1] |
| A Aᵀ−I | [3,0] |
| Squared residual | [9,0] |
| Sum | 9 |

This table traces the first worked example. Adding an identity transform as a second cloud changes the batch mean to4.5, not the per-cloud penalty.

## Gradients and interpretation

For one cloud the derivative is $4(A A^\top-I)A$. Batch averaging divides its contribution by B. Keeping ordinary tensor operations lets autograd compute this derivative; detaching would remove the training effect.

An orthogonal reflection also has zero penalty. The loss does not demand determinant+1, so it is not sufficient to enforce a physically proper SE(3) rotation. Learned feature axes need not even correspond to x,y,z.

## Why this matters on a robot

A feature transform that amplifies selected channels can make perception fragile to sensor noise. Regularization can help, but a low penalty does not prove useful segmentation or robust grasping. Record its coefficient separately from the task loss when comparing checkpoints.

## Questions and source

Why is identity zero-loss? Its rows are orthonormal. Can zero penalty guarantee a right-handed spatial frame? No: reflections are also orthogonal.

Source: [PointNet feature-transform regularization](https://arxiv.org/abs/1612.00593). This isolates the unweighted squared penalty; constructing and training the alignment network is separate.
