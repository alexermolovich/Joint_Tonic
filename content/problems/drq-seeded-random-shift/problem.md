# Apply a Seeded Random-Shift Augmentation

Small translations should not alter which physical transition a stack of camera frames represents. One seeded crop shared across time preserves relative motion while varying image placement.

## Contract

`images` is real `(B, T, H, W, C)`, with `1 <= B <= 16`, `1 <= T <= 4`, `1 <= H, W <= 64`, `1 <= C <= 3`, and values in `[0, 1]`. `padding` must be a built-in Python int in `[0, 8]`; `seed` must be a built-in Python int in `[0, 2**32 - 1]`. Booleans and NumPy integer scalars are invalid for these two arguments.

Create `rng = np.random.Generator(np.random.PCG64(seed))`. Draw `offsets = rng.integers(0, 2*padding + 1, size=(B, 2), dtype=np.int64)` exactly once, in row-offset/column-offset order. Edge-pad only height and width by `padding` on both sides. For each batch row, crop an H by W window starting at its drawn offsets. Apply that same crop to **every temporal frame and channel** in that row.

Return a dictionary with `images` (float64, original input shape) and `offsets` (int64 `(B, 2)`). With zero padding, return a fresh image copy and zero offsets. Do not interpolate, change colors, shift temporal frames independently or modify NumPy's global random state.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

An image array of shape (1, 2, 1, 1, 1), with frame values 0.2 and 0.8, remains unchanged after any padding-1 edge crop. Both frames share the same generated offset.

## Example 2

Padding 0 returns a fresh copy of the entire input and offsets [[0, 0]] for a one-row batch, for any valid seed.
