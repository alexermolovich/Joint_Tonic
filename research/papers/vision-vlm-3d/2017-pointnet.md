---
schema_version: 1
paper_id: "2017-pointnet"
title: "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation"
authors: ["Charles R. Qi", "Hao Su", "Kaichun Mo", "Leonidas J. Guibas"]
year: 2017
venue_or_status: "CVPR 2017"
primary_url: "https://arxiv.org/abs/1612.00593"
pdf_url: "https://arxiv.org/pdf/1612.00593"
local_pdf: "./2017-pointnet.pdf"
sha256: "f13e3b3c744a3977155876e2d5dcd1d0cf83c22f98ce9cc11e0a2f5e37388b6a"
bytes: 9083131
pages: 19
topics: ["point clouds", "3D classification", "3D segmentation", "permutation invariance"]
modalities: ["3D point cloud"]
track_role: "Foundational unordered 3D perception"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace."
execution_flow: {"title":"Core execution flow","description":"Transform each point with shared weights, aggregate a permutation-invariant set description, and attach either a global or point-wise prediction head.","nodes":[{"id":"stage-1","title":"Encode each point","detail":"Apply one shared feature map to every point in the cloud.","column":0,"row":0,"section":"Encode each point","problem_slugs":["pointnet-transform-regularizer","pointnet-shared-mlp","pointcloud-density-conventions"],"planned_problems":[]},{"id":"stage-2","title":"Pool the point set","detail":"Channel-wise maximum removes dependence on point ordering.","column":1,"row":0,"section":"Pool the point set","problem_slugs":["pointnet-symmetric-pooling"],"planned_problems":[]},{"id":"stage-3","title":"Classify or segment","detail":"Use a global head or combine local and global features at every point.","column":2,"row":0,"section":"Classify or segment","problem_slugs":["pointnet-local-global-features"],"planned_problems":[]}],"edges":[{"from":"stage-1","to":"stage-2","label":"point features"},{"from":"stage-2","to":"stage-3","label":"global descriptor"}]}
---

## Core paper explanation

PointNet learns directly from an unordered point set. A shared network maps each point to features, a symmetric pooling operation creates a global description, and task heads predict a set label or per-point labels. The central requirement is permutation invariance: changing the order of the same physical points must not change a global prediction. This differs from placing points into a regular voxel grid.

## Execution flow

Transform each point with shared weights, aggregate a permutation-invariant set description, and attach either a global or point-wise prediction head.

### Encode each point

Let $X\in\mathbb R^{N\times3}$ contain $N$ points expressed in one declared coordinate frame. A shared MLP produces $h(x_i)\in\mathbb R^d$ for every point. The same weights are used for all $i$, so point order does not change individual feature computation. Learned transform networks can align inputs or intermediate features.

$$
H=[h(x_1);\ldots;h(x_N)]\in\mathbb R^{N\times d}.
$$

[Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points) is a useful coordinate-frame prerequisite. A learned feature transform is not automatically a physically valid rigid-body transform.


**Prerequisite practice:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). These supporting skills do not complete this model stage.


**New runnable component:** [Regularize a Learned Feature Transform](/problems/pointnet-transform-regularizer). The exercise implements its stated bounded component with original synthetic fixtures.

**Implement these components:** [Build a Shared Point MLP and Global Feature](/problems/pointnet-shared-mlp) · [Validate Point-Cloud Density and Coordinate Conventions](/problems/pointcloud-density-conventions). Each exercise specifies its bounded scope; diagnostic and simplified variants do not reproduce the full model.

### Pool the point set

The global representation is

$$
g_j=\max_{i=1,\ldots,N}H_{ij},\qquad
f(X)=\gamma(g).
$$

For any permutation matrix $P$ over the point dimension, $f(PX)=f(X)$. The maximum is independently taken per feature channel; pooling over the feature axis instead destroys the intended invariant. A feature-transform matrix $A\in\mathbb R^{d\times d}$ is regularized toward orthogonality with

$$
R(A)=\|I-AA^\top\|_F^2.
$$

This discourages degenerate transformations but does not enforce exact orthogonality by itself.


**Implement this component:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). The symmetric pool operates on already-computed point features. It does not implement the shared MLP or alignment network.

### Classify or segment

A classification head consumes $g$. A segmentation head combines each local feature with the same global context:

$$
\hat y_i=\operatorname{softmax}\bigl(\psi([h(x_i);g])\bigr).
$$

Segmentation is permutation equivariant: permuting inputs must permute outputs the same way. It is not invariant like global classification. A clean test checks both properties and includes duplicate points, changed cloud sizes, and the documented empty-cloud policy.


**Implement this component:** [Concatenate Local and Global Features for Segmentation](/problems/pointnet-local-global-features). Feature concatenation supplies the segmentation interface, not the segmentation head.

#### Complete the feature path and audit its input

[Build the shared point MLP](/problems/pointnet-shared-mlp) supplies the missing per-point feature stage before symmetric pooling: $H=\max(0,XW+b)$ for $X\in\mathbb R^{N\times D}$, $W\in\mathbb R^{D\times F}$ and $b\in\mathbb R^F$. Its one-layer teaching contract omits T-Nets and batch normalization. [Local/global concatenation](/problems/pointnet-local-global-features) then preserves each point's identity while providing cloud context.

[Validate density and coordinate conventions](/problems/pointcloud-density-conventions) is an original data-quality diagnostic. After declared unit conversion to meter coordinates $x_i$, voxel side $h$ meters gives
$$v_i=\lfloor x_i/h\rfloor,\qquad \rho=N/|\{v_i\}|.$$
Here $\rho$ is points per occupied voxel, with zero for an empty cloud, not physical volume density. Frame compatibility is checked from explicit labels; geometry cannot establish that two frame names represent the same physical coordinates.


## Implement the components

The following bounded exercises are runnable. They use original synthetic fixtures; completing them does not reproduce the paper's training scale or headline benchmark. Systems diagnostics are explicitly identified as teaching contracts.

- [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling) — Easy.
- [Concatenate Local and Global Features for Segmentation](/problems/pointnet-local-global-features) — Easy.
- [Regularize a Learned Feature Transform](/problems/pointnet-transform-regularizer) — Easy.
- [Build a Shared Point MLP and Global Feature](/problems/pointnet-shared-mlp) — Medium.
- [Validate Point-Cloud Density and Coordinate Conventions](/problems/pointcloud-density-conventions) — Medium.

## Why this matters on a robot

Direct point processing avoids a dense 3D grid, but the basic architecture does not explicitly model local neighborhoods. Occlusion, sparse depth, and frame/scale inconsistencies can degrade recognition. Permutation invariance is not rotation invariance; coordinate preprocessing and augmentation remain important.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1612.00593) · [Open-access manuscript](https://arxiv.org/pdf/1612.00593)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
