# Build a Shared Point MLP and Global Feature

Implement `point_mlp(points: np.ndarray, weights: np.ndarray, bias: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Apply one shared affine/ReLU layer to every point, then max-pool each feature channel.
`points` has shape (N,D), 1<=N<=4096, 1<=D<=128; `weights` (D,F), 1<=F<=128; `bias` (F,). Return `(local, global_feature)` of shape (N,F) and (F,), both float64. The formula is `local=max(points @ weights + bias,0)`; global_feature is the maximum over points, independently for each feature. Empty clouds are rejected. Features are dimensionless, already normalized upstream; columns are not assumed xyz. This is a single-layer PointNet teaching block, without the T-Net, batch normalization, or learned classifier.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. `points=[[1,2],[-1,3]], weights=I₂, bias=[0,-2]` gives local `[[1,0],[0,1]]` and global `[1,1]`.
2. A single point `[[2]]`, weight `[[-3]]`, bias `[1]` gives local `[[0]]` and global `[0]`: ReLU happens before pooling.

## Source and scope

[Primary source](https://arxiv.org/abs/1612.00593). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
