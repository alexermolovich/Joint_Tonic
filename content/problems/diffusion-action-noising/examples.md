# Worked code examples

All examples use explicitly supplied noise. Re-running them must give the same output without setting a random seed.

## Example 1: two batch items at schedule endpoints

```python
import torch
from solution import diffuse_actions

actions = torch.tensor([[[2.]], [[4.]]])
noise = torch.tensor([[[10.]], [[20.]]])
noised, target = diffuse_actions(actions, torch.tensor([1.,0.]),
                                 torch.tensor([0,1]), noise)
print(noised.tolist())
print(target.tolist())
```

Expected output:

```text
[[[2.0]], [[20.0]]]
[[[10.0]], [[20.0]]]
```

At cumulative signal coefficient 1, the sample is clean; at 0, it is pure noise. The target stays the supplied noise in both cases.

## Example 2: equal signal and noise weights

```python
import torch
from solution import diffuse_actions

dtype = torch.float64
noised, target = diffuse_actions(
    torch.tensor([[[2.]]], dtype=dtype),
    torch.tensor([0.5], dtype=dtype),
    torch.tensor([0]),
    torch.tensor([[[4.]]], dtype=dtype),
)
print(f'{noised.item():.6f}', f'{target.item():.6f}')
```

Expected output:

```text
4.242641 4.000000
```

Both weights are `sqrt(0.5)`, rather than `0.5`. The target does not change to the mixed sample.

## Example 3: padded timesteps are excluded from both outputs

```python
import torch
from solution import diffuse_actions

actions = torch.tensor([[[1.,2.], [3.,4.]]])
noised, target = diffuse_actions(actions, torch.tensor([1.]),
    torch.tensor([0]), torch.ones_like(actions),
    mask=torch.tensor([[True,False]]))
print(noised.tolist())
print(target.tolist())
```

Expected output:

```text
[[[1.0, 2.0], [0.0, 0.0]]]
[[[1.0, 1.0], [0.0, 0.0]]]
```

The false mask entry covers every action channel at that horizon step.
