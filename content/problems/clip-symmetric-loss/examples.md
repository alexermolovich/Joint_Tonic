# Worked code examples

These examples format the scalar to six decimal places. The function must return a differentiable tensor, not a rounded Python number.

## Example 1: correctly paired embeddings

```python
import torch
from solution import clip_loss

images = torch.tensor([[1.,0.], [0.,1.]], dtype=torch.float64)
texts = images.clone()
loss = clip_loss(images, texts, temperature=1.0)
print(f'{loss.item():.6f}')
print(tuple(loss.shape))
```

Expected output:

```text
0.313262
()
```

Each matching logit is 1 and its negative is 0. Cross-entropy in either direction equals `log(1 + exp(-1))`.

## Example 2: swapped instructions worsen the objective

```python
import torch
from solution import clip_loss

images = torch.tensor([[1.,0.], [0.,1.]], dtype=torch.float64)
texts = torch.tensor([[0.,1.], [1.,0.]], dtype=torch.float64)
print(f'{clip_loss(images, texts, temperature=1.0).item():.6f}')
```

Expected output:

```text
1.313262
```

The diagonal still defines the pairs. The function does not relabel a batch based on whichever similarities are largest.

## Example 3: a singleton has no negatives

```python
import torch
from solution import clip_loss

images = torch.tensor([[2.,-3.]], dtype=torch.float64)
print(f'{clip_loss(images, -images).item():.6f}')
```

Expected output:

```text
0.000000
```

There is only one candidate in each direction. A valid zero loss here supplies no contrastive learning signal.
