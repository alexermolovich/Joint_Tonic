import torch


def fraction(m):
    a = torch.tensor([[[2., -2.], [4., 6.]]])
    e = torch.tensor([[[0., 2.], [2., 2.]]])
    x, u = m.flow_action_interpolants(a, e, torch.tensor([.25]), torch.tensor([[True, True]]))
    torch.testing.assert_close(x, torch.tensor([[[.5, 1.], [2.5, 3.]]]))
    torch.testing.assert_close(u, torch.tensor([[[2., -4.], [2., 4.]]]))
    assert x.dtype == u.dtype == a.dtype and x.shape == u.shape == a.shape


def endpoints(m):
    a = torch.tensor([[[2.]], [[-1.]]], dtype=torch.float64)
    e = torch.tensor([[[6.]], [[3.]]], dtype=a.dtype)
    x, u = m.flow_action_interpolants(a, e, torch.tensor([0., 1.], dtype=a.dtype), torch.ones((2, 1), dtype=torch.bool))
    torch.testing.assert_close(x, torch.tensor([[[6.]], [[-1.]]], dtype=a.dtype))
    torch.testing.assert_close(u, torch.full_like(a, -4))


def masking(m):
    a = torch.arange(12., dtype=torch.float64).reshape(2, 3, 2)
    e = -a
    v = torch.tensor([[True, False, True], [False, True, False]])
    x, u = m.flow_action_interpolants(a, e, torch.tensor([.5, .25], dtype=a.dtype), v)
    assert torch.equal(x[~v], torch.zeros_like(x[~v]))
    assert torch.equal(u[~v], torch.zeros_like(u[~v]))
    torch.testing.assert_close(u[v], 2 * a[v])
    x, u = m.flow_action_interpolants(a, e, torch.tensor([.2, .8], dtype=a.dtype), torch.zeros_like(v))
    assert torch.equal(x, torch.zeros_like(x)) and torch.equal(u, torch.zeros_like(u))


def gradients(m):
    a = torch.tensor([[[.5, .7], [-.3, .2]]], dtype=torch.float64, requires_grad=True)
    e = torch.tensor([[[.2, -.4], [.4, 1.]]], dtype=a.dtype, requires_grad=True)
    t = torch.tensor([.3], dtype=a.dtype, requires_grad=True)
    v = torch.tensor([[True, False]])
    assert torch.autograd.gradcheck(lambda aa, ee, tt: m.flow_action_interpolants(aa, ee, tt, v), (a, e, t))
    x, u = m.flow_action_interpolants(a, e, t, v)
    (x.sum() + u.sum()).backward()
    assert torch.equal(a.grad[:, 1], torch.zeros_like(a.grad[:, 1]))
    assert torch.equal(e.grad[:, 1], torch.zeros_like(e.grad[:, 1]))
    torch.testing.assert_close(t.grad, (a.detach() - e.detach())[:, 0].sum().reshape(1))


def noncontiguous(m):
    a = torch.arange(24., dtype=torch.float64).reshape(2, 3, 4).transpose(1, 2)
    e = -a
    t = torch.tensor([.2, 9., .8, 9.], dtype=a.dtype)[::2]
    v = torch.ones((4, 2), dtype=torch.bool).t()
    before = [z.clone() for z in (a, e, t, v)]
    x, u = m.flow_action_interpolants(a, e, t, v)
    torch.testing.assert_close(x[0], -.6 * a[0]); torch.testing.assert_close(x[1], .6 * a[1])
    for actual, copy in zip((a, e, t, v), before): torch.testing.assert_close(actual, copy)
    assert x.data_ptr() not in (a.data_ptr(), e.data_ptr(), u.data_ptr())
    assert u.data_ptr() not in (a.data_ptr(), e.data_ptr())


def scale(m):
    a = torch.full((16, 128, 32), 1e6)
    e = -a
    x, u = m.flow_action_interpolants(a, e, torch.full((16,), .5), torch.ones((16, 128), dtype=torch.bool))
    assert torch.equal(x, torch.zeros_like(x))
    torch.testing.assert_close(u, torch.full_like(a, 2e6))


def expect(error, fn):
    try:
        fn()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def contracts(m):
    a = torch.zeros((1, 2, 2)); e = a.clone(); t = torch.tensor([.5]); v = torch.tensor([[True, False]])
    for i in range(4):
        args = [a, e, t, v]; args[i] = args[i].tolist()
        expect(TypeError, lambda args=args: m.flow_action_interpolants(*args))
    for bad in (torch.tensor(.5), torch.tensor([-.1]), torch.tensor([1.1]), torch.tensor([float("nan")]), t.double(), torch.ones((2,))):
        expect(ValueError, lambda bad=bad: m.flow_action_interpolants(a, e, bad, v))
    for bad in (e.long(), e.double(), e[0], e[:, :, :1], torch.full_like(e, float("inf")), torch.full_like(e, 1e6 + 1)):
        expect(ValueError, lambda bad=bad: m.flow_action_interpolants(a, bad, t, v))
    expect(ValueError, lambda: m.flow_action_interpolants(a, e, t, v.float()))
    nan_padding = a.clone(); nan_padding[:, 1] = float("nan")
    expect(ValueError, lambda: m.flow_action_interpolants(nan_padding, e, t, v))
    expect(ValueError, lambda: m.flow_action_interpolants(torch.zeros((1, 0, 2)), torch.zeros((1, 0, 2)), t, torch.zeros((1, 0), dtype=torch.bool)))


TESTS = [
    ("Fractional flow time", "public", fraction),
    ("Per-example endpoints", "public", endpoints),
    ("Mask both outputs, including all padding", "hidden", masking),
    ("Action, noise and flow-time gradients", "hidden", gradients),
    ("Noncontiguous storage and immutability", "hidden", noncontiguous),
    ("Realistic tensor size", "hidden", scale),
    ("Input contracts and invalid padding", "hidden", contracts),
]
