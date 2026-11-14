import torch


def padded_example(m):
    p = torch.tensor([[[1., 3.], [100., 100.]]], requires_grad=True)
    t = torch.tensor([[[0., 1.], [0., 0.]]])
    loss = m.conditional_noise_loss(p, t, torch.tensor([[True, False]]))
    assert isinstance(loss, torch.Tensor) and loss.shape == () and loss.dtype == p.dtype
    torch.testing.assert_close(loss, torch.tensor(2.5))
    loss.backward(); torch.testing.assert_close(p.grad, torch.tensor([[[1., 2.], [0., 0.]]]))


def global_mean(m):
    p = torch.tensor([[[2.], [0.]], [[2.], [4.]]], dtype=torch.float64)
    loss = m.conditional_noise_loss(p, torch.zeros_like(p), torch.tensor([[True, False], [True, True]]))
    torch.testing.assert_close(loss, torch.tensor(8., dtype=p.dtype))


def gradients(m):
    p = torch.tensor([[[.2, -.3], [1., 2.]]], dtype=torch.float64, requires_grad=True)
    target = torch.tensor([[[.7, .2], [3., -4.]]], dtype=p.dtype, requires_grad=True)
    v = torch.tensor([[True, False]])
    assert torch.autograd.gradcheck(lambda a, b: m.conditional_noise_loss(a, b, v), (p, target))
    m.conditional_noise_loss(p, target, v).backward()
    torch.testing.assert_close(p.grad, -target.grad)
    assert torch.equal(p.grad[:, 1], torch.zeros_like(p.grad[:, 1]))


def noncontiguous(m):
    p = torch.arange(24., dtype=torch.float64).reshape(2, 3, 4).transpose(1, 2)
    target = p.flip(0).clone()
    v = torch.tensor([[True, False], [False, True], [True, True], [True, False]]).t()
    before = [x.clone() for x in (p, target, v)]
    loss = m.conditional_noise_loss(p, target, v)
    torch.testing.assert_close(loss, ((p - target)[v].square()).mean())
    for value, copy in zip((p, target, v), before): torch.testing.assert_close(value, copy)
    assert loss.data_ptr() not in (p.data_ptr(), target.data_ptr())


def scale_and_bounds(m):
    p = torch.full((32, 128, 32), 1e6)
    t = -p
    v = torch.ones((32, 128), dtype=torch.bool)
    result = m.conditional_noise_loss(p, t, v)
    torch.testing.assert_close(result, torch.tensor(4e12), rtol=1e-6, atol=0)
    assert torch.isfinite(result)


def expect(error, fn):
    try:
        fn()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def contracts(m):
    p = torch.zeros((1, 2, 2)); v = torch.tensor([[True, False]])
    for index in range(3):
        args = [p, p.clone(), v]; args[index] = args[index].tolist()
        expect(TypeError, lambda args=args: m.conditional_noise_loss(*args))
    for bad in (p.long(), p.double(), p[0], p[:, :0], p[:, :, :1], torch.full_like(p, 1e6 + 1), torch.full_like(p, float("nan"))):
        expect(ValueError, lambda bad=bad: m.conditional_noise_loss(p, bad, v))
    for bad in (v.float(), v[0], torch.zeros_like(v)):
        expect(ValueError, lambda bad=bad: m.conditional_noise_loss(p, p, bad))
    nan_padding = p.clone(); nan_padding[:, 1] = float("nan")
    expect(ValueError, lambda: m.conditional_noise_loss(nan_padding, p, v))
    expect(ValueError, lambda: m.conditional_noise_loss(torch.zeros((65, 1, 1)), torch.zeros((65, 1, 1)), torch.ones((65, 1), dtype=torch.bool)))


TESTS = [
    ("Padding and prediction gradient", "public", padded_example),
    ("Global scalar mean", "public", global_mean),
    ("Gradients through both floating inputs", "hidden", gradients),
    ("Noncontiguous tensors and immutability", "hidden", noncontiguous),
    ("Finite loss at realistic scale", "hidden", scale_and_bounds),
    ("Types, bounds and invalid padding", "hidden", contracts),
]
