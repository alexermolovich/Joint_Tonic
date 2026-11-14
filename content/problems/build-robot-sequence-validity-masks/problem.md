# Build Padding and Validity Masks for Robot Sequences

Build valid-token and causal-attention masks for padded robot episodes.

```python
def sequence_masks(lengths, max_steps):
```

## Contract

Lengths must be nonnegative integer-valued entries <=max_steps. max_steps is an integer in [0,512], not bool. B<=128. A token is valid when its index is less than its episode length. Attention[b,i,j] is true exactly when both i and j are valid and j<=i. True means allowed, not blocked. Empty batches and zero-length episodes are valid.

**Shapes and outputs:** lengths(B,) -> valid bool(B,T), attention bool(B,T,T), T=max_steps.

**Units:** lengths: frames, max_steps: frames. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[2,0], max_steps=3` → valid `[[True,True,False],[False,False,False]]`; the first attention matrix is the table above, the second is all false.
2. `lengths=[1], max_steps=1` → valid `[[True]]`, attention `[[[True]]]`.
