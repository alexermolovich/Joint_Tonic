# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](statement.md) is the complete contract.

## Example 1: independent row norms

```python
images = torch.tensor([[3., 4.], [0., -2.]], dtype=torch.float64)
texts  = torch.tensor([[0., 5.], [-8., 6.]], dtype=torch.float64)
normalize_clip_embeddings(images, texts)
# (tensor([[0.6, 0.8], [0.0, -1.0]], dtype=torch.float64),
#  tensor([[0.0, 1.0], [-0.8, 0.6]], dtype=torch.float64))
```

Image row norms are 5 and 2; text row norms are 5 and 10. Negative feature components remain negative.

## Example 2: equal directions, different magnitudes

```python
images = torch.tensor([[2., 0., 0.], [20., 0., 0.]], dtype=torch.float32)
texts  = torch.tensor([[0., 0., -7.], [0., 0., -0.5]], dtype=torch.float32)
normalize_clip_embeddings(images, texts)
# (tensor([[1., 0., 0.], [1., 0., 0.]]),
#  tensor([[0., 0., -1.], [0., 0., -1.]]))
```

Positive rescaling changes length but not normalized direction. Neither example changes the image-to-caption row pairing.

## Theory question answers

1. Yes. A per-column norm mixes samples and changes when unrelated rows change; the required per-row norm does not.
2. The encoder must receive the normalization derivative through autograd. Detaching destroys that connection.
