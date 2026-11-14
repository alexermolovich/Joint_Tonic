# Fuse Temporal BEV State

Implement `fuse_bev(current: np.ndarray, history: np.ndarray, history_valid: np.ndarray, gate: np.ndarray, reset: bool) -> np.ndarray`.

Fuse already aligned BEV history with current features using a supplied scalar gate per cell.
`current` and `history` are float64 (H,W,D), 1<=H,W<=128,1<=D<=64. `history_valid` is bool (H,W), `gate` float64 (H,W) in [0,1], and reset is a built-in bool. Return float64 (H,W,D). At valid cells and reset=False use `(1-gate)*current+gate*history`; otherwise copy current exactly. All inputs including ignored history must be finite and valid. The history has already been warped into the current ego grid; feature channels are dimensionless. Reset marks a sequence boundary. This deterministic gated teaching substitute exposes temporal state rules; it is not BEVFormer's learned temporal self-attention.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. current=`[[[2,4]]]`, history=`[[[10,0]]]`, valid=`[[True]]`, gate=`[[0.25]]`, reset=False returns `[[[4,3]]]`.
2. With those same inputs and reset=True, output is `[[[2,4]]]`. An invalid history cell also returns current regardless of its gate.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
