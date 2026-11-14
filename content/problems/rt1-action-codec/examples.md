# Worked code examples

The snippets print lists for both outputs. The function itself returns int64 tokens and float64 reconstructed actions.

## Example 1: endpoints and an internal boundary

```python
from solution import action_codec

tokens, decoded = action_codec([[-1.], [0.], [1.]], [-1.], [1.], bins=4)
print(tokens.tolist())
print(decoded.tolist())
print(str(tokens.dtype), str(decoded.dtype))
```

Expected output:

```text
[[0], [2], [3]]
[[-0.75], [0.25], [0.75]]
int64 float64
```

Zero lies on the upper edge of bin 1 and enters bin 2. The upper bound is clipped to bin 3 rather than producing invalid bin 4.

## Example 2: clipping plus reserved tokens

```python
from solution import action_codec

tokens, decoded = action_codec([[-5.,9.]], [0.,0.], [2.,8.],
                               bins=2, token_offset=100)
print(tokens.tolist())
print(decoded.tolist())
```

Expected output:

```text
[[100, 101]]
[[0.5, 6.0]]
```

Clipping occurs per dimension. Vocabulary offset 100 does not change the physical bin centers.

## Example 3: an unbatched multi-channel action

```python
from solution import action_codec

tokens, decoded = action_codec([0.25,0.75], [0.,0.], [1.,1.], bins=2)
print(tokens.tolist(), decoded.tolist())
print(tokens.shape, decoded.shape)
```

Expected output:

```text
[0, 1] [0.25, 0.75]
(2,) (2,)
```

The final axis is the action dimension. An unbatched action does not gain an extra batch axis.
