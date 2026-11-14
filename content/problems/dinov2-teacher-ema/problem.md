# Update a Teacher Encoder with Exponential Moving Average

Produce a detached teacher-parameter snapshot from matched teacher/student names and one EMA momentum.

```python
def update_teacher_ema(teacher: dict[str, torch.Tensor],
                       student: dict[str, torch.Tensor],
                       momentum: float) -> dict[str, torch.Tensor]:
```

## Contract

Return a new dictionary of teacher parameters using `new_teacher[name] = momentum*teacher[name] + (1-momentum)*student[name]`. The student tensors represent the **post-optimizer-step** student. Apply exactly one update; do not advance a schedule or update the student.

Both arguments must be Python dictionaries with exactly the same nonempty-string keys. The empty dictionary is valid and returns `{}`. Pair by name, never by dictionary position. Values must be finite CPU PyTorch tensors with dtype `float32` or `float64`; each teacher/student pair must share dtype and exact shape. Different names may have different shapes or dtypes. Scalar and zero-element tensors are supported. Each dictionary has at most `1_000_000` total tensor elements.

`momentum` is a finite Python `int` or `float`, excluding booleans, in `[0,1]`. Zero copies the student values; one copies the teacher values. These endpoints are software boundary cases; the usual training update uses momentum below one.

Return keys in teacher insertion order. Each output tensor keeps its corresponding shape/dtype/device but has independent storage, `requires_grad=False`, and no gradient function, even when an input requires gradients. Neither dictionary nor any input tensor may be mutated. The new parameters are a snapshot, not a differentiable output used to optimize the teacher. A Python loop over names is allowed.

Inputs contain **parameters only**, not an arbitrary `state_dict`. Buffers, running statistics, optimizer state, centers, and integer counters are out of scope and must not be mixed into this API. Integer/bool tensors are rejected rather than averaged or copied by a hidden rule.

Raise `TypeError` for a non-dictionary argument or a non-tensor value. Raise `ValueError` for all other violations, including key mismatch, invalid names, wrong dtype/shape/device, nonfinite values, or invalid momentum. Tests supply one violation at a time. Parameter coordinates are not robot frames; one update corresponds to one explicit training step, not seconds.

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

## Runtime

Python 3.12.3 on the local CPU sandbox. The shared worker enforces 18 seconds wall time, 10 seconds CPU, 4 GiB address space, and 64 KiB output. Dependency versions are pinned in this problem’s metadata. No GPU, downloaded model, or external dataset is required.

## Hints

## Hint 1

Check that the two key sets agree, then look up the student tensor using each teacher name. Zipping dictionary values is unsafe.

## Hint 2

Perform the update without creating an autograd graph. Returning student directly at momentum zero would violate both detachment and independent-storage requirements.

## Hint 3

Treat buffers as a separate contract rather than guessing which integer entries to copy. Empty dictionaries and scalar parameter tensors still have well-defined behavior.
