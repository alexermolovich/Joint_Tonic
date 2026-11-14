# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](statement.md) is the complete contract.

## Example 1: a slow teacher update

```python
teacher = {'weight': torch.tensor([2., 4.], dtype=torch.float64),
           'bias': torch.tensor(1., dtype=torch.float64)}
student = {'bias': torch.tensor(3., dtype=torch.float64),
           'weight': torch.tensor([6., 0.], dtype=torch.float64)}
update_teacher_ema(teacher, student, 0.9)
# {'weight': tensor([2.4, 3.6], dtype=torch.float64),
#  'bias': tensor(1.2, dtype=torch.float64)}
```

Dictionary order differs, so names must identify the pairs. The weight update is `0.9*[2,4] + 0.1*[6,0]`.

## Example 2: an endpoint still returns a detached copy

```python
teacher = {'weight': torch.tensor([-1., 2.])}
student = {'weight': torch.tensor([5., 7.], requires_grad=True)}
result = update_teacher_ema(teacher, student, 0.0)
# {'weight': tensor([5., 7.])}
result['weight'].requires_grad
# False
```

The output values equal the student, but the tensor is not the student tensor and shares no storage. Changing `result['weight']` afterwards must not change either input. With momentum `1.0`, the same inputs produce a fresh `[-1,2]` teacher copy.

## Theory question answers

1. Different names can be combined without any shape error; match by name instead.
2. No. Values stay the same, but the contract still requires a new dictionary and independent detached tensor storage.
