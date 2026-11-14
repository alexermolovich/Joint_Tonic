# Blend Overlapping Action Chunks with Temporal Ensembling

Draft for review; this is not a published or runnable problem.

## Task

Several chunks may predict an action for the same target control tick. Select the corresponding horizon entry from every eligible chunk, then blend those predictions using exponentially decreasing weights ordered oldest to newest.

## Function

```python
def temporal_ensemble(
    predictions: np.ndarray,
    start_ticks: np.ndarray,
    valid: np.ndarray,
    target_tick: int,
    decay: float,
) -> tuple[np.ndarray, np.ndarray]:
    ...
```

- `predictions`: float32 or float64 NumPy array `(C,H,D)`; all entries finite with absolute value at most `1e6`, including masked positions. `0<=C<=256`, `1<=H<=256`, `1<=D<=64`, and at most `2_000_000` elements.
- `start_ticks`: int64 NumPy array `(C,)`, strictly increasing, with values in `[0,1_000_000]`.
- `valid`: bool NumPy array `(C,H)`. True means that prediction is available; validity must not be inferred from action values.
- `target_tick`: built-in non-bool int in `[0,1_000_000]`. `decay`: built-in non-bool int or float, finite and in `[0,100]`.
- Chunk `c` is eligible only if `h=target_tick-start_ticks[c]` satisfies `0<=h<H` and `valid[c,h]` is True. Future chunks and expired horizons are ineligible.
- Rank eligible chunks from oldest to newest using ranks `i=0..M-1`, ignoring ineligible rows. Weight rank `i` by `exp(-decay*i)`, then normalize across eligible chunks. This is **rank**, not elapsed tick difference.
- Return `(action, weights)`. `action` is shape `(D,)`; `weights` is shape `(C,)` with exactly zero for ineligible chunks. Both use the predictions’ float dtype, CPU NumPy storage, and are fresh arrays not aliasing inputs. Compute weights and accumulation in float64, then cast both outputs to the input dtype.
- Noncontiguous arrays are accepted. No input mutation, sorting, randomness, or fallback action is allowed. At least one eligible chunk is required; `C=0` is therefore an error after shape validation.

All predictions must describe the same normalized Euclidean action channels, frame, and controller. This function does not average quaternions or circular angles. A valid zero-valued action participates normally.

## Errors and complexity

Raise `TypeError` for non-array array arguments or invalid scalar types, including bool. Raise `ValueError` for all array-contract violations, scalar range/finiteness errors, nonincreasing starts, size caps, or no eligible predictions.

Input validation is `O(CHD)`; selection/blending is `O(CD)` with `O(C+D)` output/working storage after validation. The oldest eligible rank has unnormalized weight1, so large decay must not yield a zero denominator.

## Worked examples

### Case1: three chunks predicting tick2

```text
predictions = [[[0],[0],[2]], [[0],[4],[0]], [[8],[0],[0]]]
start_ticks = [0,1,2]   # int64
valid = [[True,True,True], [True,True,True], [True,True,True]]
target_tick = 2
decay = ln(2)

action = [24/7]         # approximately3.4285714286
weights = [4/7,2/7,1/7]
```

Selected entries are predictions[0,2]=2, predictions[1,1]=4, and predictions[2,0]=8. Raw weights are1,1/2,1/4. The oldest prediction receives the largest weight.

### Case2: a real zero prediction remains eligible

```text
predictions = [[[7],[7],[0]], [[10],[20],[30]]]
start_ticks = [5,7]   # int64
valid = [[True,True,True], [True,True,True]]
target_tick = 7
decay = 0

action = [5]
weights = [0.5,0.5]
```

The selected values are0 and10. Their mean is5; excluding a zero-valued prediction would incorrectly return10.

## Source and scope

This exercise implements ACT’s temporal ensembling after chunk predictions already exist. It follows the primary paper’s oldest-first rank convention. Explicit validity masks, nonconsecutive start ticks, and returned diagnostic weights are teaching extensions; normalized Euclidean channels exclude quaternion averaging and wrapped-angle interpolation.

[Primary paper](https://arxiv.org/abs/2304.13705).
