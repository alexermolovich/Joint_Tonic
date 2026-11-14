# Build Sliding Action Chunks with Padding Masks

Implement this component in the local CPU workspace.

## Task

Given one recorded action sequence and requested start indices, return one fixed-length future action chunk per start. Copy available actions; fill positions beyond the episode end with zeros and mark those positions invalid.

## Function

```python
def sliding_action_chunks(
    actions: np.ndarray, start_indices: np.ndarray, horizon: int
) -> tuple[np.ndarray, np.ndarray]:
    ...
```

- `actions`: float32 or float64 NumPy array `(T,D)`. Entries must be finite with magnitude at most `1e6`. `1<=T<=10000`, `1<=D<=64`.
- `start_indices`: int64 NumPy array `(S,)`, with `0<=S<=4096` and every value in `[0,T)`. Unsorted or repeated starts are valid. A zero-length array is valid.
- `horizon`: built-in Python int, excluding bool, in `[1,256]`. Require `S*horizon*D<=2_000_000`.
- Return `(chunks, valid)`. `chunks` has shape `(S,horizon,D)` and the input float dtype. `valid` has shape `(S,horizon)` and NumPy bool dtype. Both are fresh arrays sharing no storage with inputs.
- For requested start `s=start_indices[i]` and offset `h`, copy `actions[s+h]` exactly when `s+h<T`. Otherwise write an all-zero action vector and `False`. A recorded zero action remains valid.
- For empty starts, return shapes `(0,horizon,D)` and `(0,horizon)`. Noncontiguous inputs are supported; do not mutate inputs or sort starts.

The action channel order, units, and frame are unchanged. Consecutive rows correspond to a fixed control interval selected by the caller. Padding is missing target data, not a stop command; it must not be sent to a robot or treated as a valid training target.

## Errors

Raise `TypeError` for non-array actions/start_indices or a horizon that is not a built-in non-bool int. Raise `ValueError` for array shape/dtype/value violations, invalid start indices, out-of-range horizon, empty action dimensions, or the output-size cap. Float arrays for indices are rejected even when values look integral.

Output construction takes `O(S*H*D)` time and memory, plus `O(T*D+S)` input validation. The function draws no randomness.

## Worked examples

### Case1: a complete window and a padded tail

```text
actions = [[1],[2],[3]]
start_indices = [0,2]   # int64
horizon = 2

chunks = [[[1],[2]], [[3],[0]]]
valid = [[True,True], [True,False]]
```

The second window begins at the last real action. Its second slot has no target, so it is zero and invalid.

### Case2: preserve unsorted duplicate starts

```text
actions = [[2,-1],[4,3]]
start_indices = [1,0,1]   # int64
horizon = 3

chunks = [
  [[4,3],[0,0],[0,0]],
  [[2,-1],[4,3],[0,0]],
  [[4,3],[0,0],[0,0]]
]
valid = [[True,False,False], [True,True,False], [True,False,False]]
```

There is no deduplication or sorting. Every output row corresponds to the same-position entry of start_indices.

## Source and scope

ACT motivates predicting future action chunks. This exercise only builds supervised target windows from one recorded episode. Zero right-padding and True=valid masks are explicit educational conventions; no CVAE, policy inference, or cross-episode concatenation is implemented.

[Primary paper](https://arxiv.org/abs/2304.13705).


## Progressive hints

## Hint 1

Construct each requested index as start_indices[:,None]+arange(horizon)[None,:]. Derive validity before gathering.

## Hint 2

Out-of-range indices must not reach array indexing. Use safe temporary indices or copy only valid entries, then set invalid entries to zero.

## Hint 3

Preserve start order and duplicates. Allocate independent outputs so a view of actions cannot leak mutations into the recorded dataset.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=1e-6 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
