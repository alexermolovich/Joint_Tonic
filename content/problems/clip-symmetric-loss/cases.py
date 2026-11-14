"""Deterministic synthetic tests; fixtures licensed CC0-1.0."""
import math
import torch


def _raises(kind, callback):
    try:
        callback()
    except kind:
        return
    raise AssertionError(f"expected {kind.__name__}")


def aligned(m):
    x = torch.eye(2, dtype=torch.float64)
    result = m.clip_loss(x, x, 1.0)
    torch.testing.assert_close(result, torch.tensor(math.log1p(math.exp(-1)), dtype=x.dtype))


def swapped(m):
    x = torch.eye(2)
    result = m.clip_loss(x, x.flip(0), 1.0)
    torch.testing.assert_close(result, torch.tensor(math.log1p(math.e)))


def singleton(m):
    x = torch.tensor([[2., -3.]])
    assert m.clip_loss(x, -x).shape == ()
    torch.testing.assert_close(m.clip_loss(x, -x), torch.tensor(0.))


def scale_invariance(m):
    a = torch.tensor([[1., 2.], [-2., 3.], [4., -1.]], dtype=torch.float64)
    b = a.roll(1, 0)
    torch.testing.assert_close(m.clip_loss(a * 7, b * 0.3, 0.7), m.clip_loss(a, b, 0.7))


def two_directions(m):
    a = torch.tensor([[1., 2.], [2., -1.], [1., 1.]], dtype=torch.float64)
    b = torch.tensor([[2., 1.], [-1., 3.], [1., -2.]], dtype=torch.float64)
    z = a / a.norm(dim=1, keepdim=True)
    w = b / b.norm(dim=1, keepdim=True)
    logits = z @ w.T / 0.4
    expected = (-2 * logits.diag() + logits.logsumexp(0) + logits.logsumexp(1)).mean() / 2
    torch.testing.assert_close(m.clip_loss(a, b, 0.4), expected)


def gradients(m):
    a = torch.tensor([[1., 2.], [2., -1.]], dtype=torch.float64, requires_grad=True)
    b = torch.tensor([[2., 1.], [1., -3.]], dtype=torch.float64, requires_grad=True)
    result = m.clip_loss(a, b, 0.8)
    assert result.dtype == a.dtype and result.device == a.device
    result.backward()
    assert a.grad is not None and b.grad is not None
    assert torch.isfinite(a.grad).all() and torch.isfinite(b.grad).all()
    assert a.grad.abs().sum() > 0 and b.grad.abs().sum() > 0
    delta = 1e-6
    plus, minus = a.detach().clone(), a.detach().clone()
    plus[0, 0] += delta
    minus[0, 0] -= delta
    numerical = (m.clip_loss(plus, b.detach(), 0.8) - m.clip_loss(minus, b.detach(), 0.8)) / (2 * delta)
    torch.testing.assert_close(a.grad[0, 0], numerical, rtol=1e-4, atol=1e-6)


def stability_and_immutability(m):
    a = torch.tensor([[1., 0.], [0., 1.]], requires_grad=True)
    b = a.detach().flip(0).clone().requires_grad_()
    old_a, old_b = a.detach().clone(), b.detach().clone()
    result = m.clip_loss(a, b, 0.001)
    assert torch.isfinite(result)
    result.backward()
    assert torch.isfinite(a.grad).all()
    torch.testing.assert_close(a.detach(), old_a)
    torch.testing.assert_close(b.detach(), old_b)


def invalid_temperature(m):
    x = torch.eye(2)
    for t in (0, -1, float("nan"), float("inf"), True):
        _raises(ValueError, lambda: m.clip_loss(x, x, t))


def invalid_features(m):
    x = torch.eye(2)
    for bad in (torch.ones(3, 2), torch.ones(2, 2, 1), torch.empty(0, 2), x.double()):
        _raises(ValueError, lambda: m.clip_loss(x, bad))
    _raises(ValueError, lambda: m.clip_loss(x, torch.zeros_like(x)))
    _raises(ValueError, lambda: m.clip_loss(x.long(), x.long()))
    _raises(ValueError, lambda: m.clip_loss(x, x * float("nan")))
    _raises(TypeError, lambda: m.clip_loss([[1., 0.]], x))


TESTS = [
    ("Aligned orthogonal pairs", "public", aligned),
    ("Swapped text pairs", "public", swapped),
    ("Singleton batch", "public", singleton),
    ("Positive-scale invariance", "hidden", scale_invariance),
    ("Both retrieval directions", "hidden", two_directions),
    ("Autograd and finite differences", "hidden", gradients),
    ("Stable logits and unchanged inputs", "hidden", stability_and_immutability),
    ("Temperature validation", "hidden", invalid_temperature),
    ("Feature contract errors", "hidden", invalid_features),
]
