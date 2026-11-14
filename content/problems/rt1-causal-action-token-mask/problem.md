# Build a Causal Action-Token Mask

Implement this component in the local CPU workspace.

## Task

Build an allowed-attention matrix for a sequence containing `T` timesteps. Each timestep stores `V` visual tokens followed by `A` action slots:

```text
[visual(t0), action(t0), visual(t1), action(t1), ...]
```

For query row `i` and key column `j`, allow attention exactly when `j<=i` and the two positions are not both action slots. This is a structural mask, not an additive negative-infinity mask.

## Function

```python
def rt1_attention_mask(
    steps: int, visual_tokens: int, action_tokens: int
) -> np.ndarray:
    ...
```

All three arguments must be built-in Python `int` values, excluding `bool`. Each must be positive and at most `1024`; their combined length `L=steps*(visual_tokens+action_tokens)` must be at most `1024`.

Return a fresh NumPy bool array `(L,L)`. `True` means allowed. No randomness, tensor backend, padding, or device argument is involved. Time and output memory are `O(L²)`.

## Important row semantics

- Visual queries see all earlier slots and themselves, including earlier action placeholders.
- Action queries see only visual slots at or before their own position. They cannot see any action slot, including themselves or earlier timesteps’ action slots.
- Every future key is blocked. Visual tokens within a timestep remain ordered causally rather than becoming a bidirectional visual block.
- The reference RT-1 input action embeddings are zeroed. Do not claim that this mask by itself prevents every indirect label leak when nonzero teacher-forced action labels are inserted.

## Errors

Raise `TypeError` for a non-built-in-int argument, including booleans, NumPy integer scalars, floats, or strings. Raise `ValueError` for a nonpositive/out-of-range integer or combined length above `1024`. Empty sequences and zero-token groups are not supported.

## Worked examples

### Case1: one visual block followed by action slots

```text
steps=1, visual_tokens=2, action_tokens=2
slot labels: [V0.0,V0.1,A0.0,A0.1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,1,0,0],
 [1,1,0,0],
 [1,1,0,0]]
```

The second visual query sees the first visual key and itself. Both action queries see both visual keys, but neither sees action keys.

### Case2: a later visual query can see an earlier placeholder

```text
steps=2, visual_tokens=1, action_tokens=1
slot labels: [V0,A0,V1,A1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,0,0,0],
 [1,1,1,0],
 [1,0,1,0]]
```

The row for V1 includes A0. The row for A1 excludes A0 and A1. This is intentional reference behavior; replacing every action-key column with zeros would produce a different mask.

## Source and scope

This exercise reproduces the structural mask in the pinned official RT-1 implementation using a NumPy boolean output. It omits token embedding, shifted prediction readouts, sequence padding, and the transformer. The reference implementation zeroes input action embeddings; this mask alone is not a license to insert teacher-forced action labels.

[Primary paper](https://arxiv.org/abs/2212.06817) · [Verified implementation reference](https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L161-L196).


## Progressive hints

## Hint 1

Use position modulo visual_tokens+action_tokens to determine token type. Do not infer type from the timestep alone.

## Hint 2

Start with the causal relation key_index<=query_index, then form the outer AND of action-slot indicators.

## Hint 3

Clear the action/action cells only. Check the V1 row from Case2 to catch the tempting but incorrect rule that blocks every action-key column.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=1e-6 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
