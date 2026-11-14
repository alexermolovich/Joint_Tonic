"""Deterministic supplied-noise fixtures; CC0-1.0."""
import torch


def _raises(kind, fn):
    try:
        fn()
    except kind:
        return
    raise AssertionError(f"expected {kind.__name__}")


def endpoints(m):
    a = torch.tensor([[[2.]], [[4.]]])
    e = torch.tensor([[[10.]], [[20.]]])
    x, target = m.diffuse_actions(a, torch.tensor([1., 0.]), torch.tensor([0, 1]), e)
    torch.testing.assert_close(x, torch.tensor([[[2.]], [[20.]]]))
    torch.testing.assert_close(target, e)


def manual(m):
    x, target = m.diffuse_actions(torch.tensor([[[2.]]]), torch.tensor([0.5]),
                                  torch.tensor([0]), torch.tensor([[[4.]]]))
    torch.testing.assert_close(x, torch.tensor([[[4.242640687]]]))
    torch.testing.assert_close(target, torch.tensor([[[4.]]]))


def masking(m):
    a = torch.tensor([[[1., 2.], [3., 4.]]])
    e = torch.ones_like(a)
    x, target = m.diffuse_actions(a, torch.tensor([1.]), torch.tensor([0]), e, torch.tensor([[True, False]]))
    torch.testing.assert_close(x, torch.tensor([[[1., 2.], [0., 0.]]]))
    torch.testing.assert_close(target, torch.tensor([[[1., 1.], [0., 0.]]]))


def batched_broadcast(m):
    a = torch.arange(24, dtype=torch.float64).reshape(2, 3, 4)
    e = -torch.ones_like(a)
    x, target = m.diffuse_actions(a, torch.tensor([1., 0.64, 0.], dtype=a.dtype),
                                  torch.tensor([1, 2]), e)
    torch.testing.assert_close(x[0], 0.8 * a[0] - 0.6)
    torch.testing.assert_close(x[1], e[1])
    assert x.dtype == target.dtype == a.dtype


def gradients(m):
    a = torch.ones((2, 3, 2), dtype=torch.float64, requires_grad=True)
    e = torch.ones_like(a, requires_grad=True)
    x, target = m.diffuse_actions(a, torch.tensor([0.64], dtype=a.dtype), torch.tensor([0, 0]), e)
    x.sum().backward()
    torch.testing.assert_close(a.grad, torch.full_like(a, 0.8))
    torch.testing.assert_close(e.grad, torch.full_like(e, 0.6))


def unchanged(m):
    a = torch.ones((1, 2, 3))
    e = torch.arange(6.).reshape(1, 2, 3)
    mask = torch.tensor([[False, True]])
    old_a, old_e, old_mask = a.clone(), e.clone(), mask.clone()
    m.diffuse_actions(a, torch.tensor([0.3]), torch.tensor([0]), e, mask)
    torch.testing.assert_close(a, old_a)
    torch.testing.assert_close(e, old_e)
    torch.testing.assert_close(mask, old_mask)


def invalid_schedule(m):
    a = torch.ones(1, 2, 2)
    for schedule in (torch.tensor([]), torch.tensor([0.2, 0.5]), torch.tensor([-0.1]),
                     torch.tensor([float("nan")]), torch.tensor([[0.4]])):
        _raises(ValueError, lambda: m.diffuse_actions(a, schedule, torch.tensor([0]), a))


def invalid_steps_mask(m):
    a = torch.ones(1, 2, 2)
    s = torch.tensor([0.5])
    for steps in (torch.tensor([1]), torch.tensor([-1]), torch.tensor([0.]), torch.tensor([0, 0])):
        _raises(ValueError, lambda: m.diffuse_actions(a, s, steps, a))
    for mask in (torch.ones(1, 2), torch.ones(1, 2, 1, dtype=torch.bool)):
        _raises(ValueError, lambda: m.diffuse_actions(a, s, torch.tensor([0]), a, mask))


def invalid_inputs(m):
    a = torch.ones(1, 2, 2)
    _raises(ValueError, lambda: m.diffuse_actions(a, torch.tensor([0.5]).double(), torch.tensor([0]), a))
    _raises(ValueError, lambda: m.diffuse_actions(a, torch.tensor([0.5]), torch.tensor([0]), a * float("inf")))
    _raises(ValueError, lambda: m.diffuse_actions(a.long(), torch.tensor([0.5]), torch.tensor([0]), a.long()))
    _raises(TypeError, lambda: m.diffuse_actions([], torch.tensor([0.5]), torch.tensor([0]), a))


TESTS = [
    ("Signal and noise endpoints", "public", endpoints),
    ("Equal-weight numerical example", "public", manual),
    ("Masked padding", "public", masking),
    ("One timestep per batch item", "hidden", batched_broadcast),
    ("Preserve action and noise gradients", "hidden", gradients),
    ("Leave all inputs unchanged", "hidden", unchanged),
    ("Validate cumulative schedule", "hidden", invalid_schedule),
    ("Validate timestep and mask axes", "hidden", invalid_steps_mask),
    ("Validate numeric tensor contract", "hidden", invalid_inputs),
]
