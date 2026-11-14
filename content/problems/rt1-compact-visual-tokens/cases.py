import math
import torch


def example(m):
    f = torch.tensor([[[1., 0.], [3., 2.], [9., 9.]]], dtype=torch.float64)
    l = torch.tensor([[[0., math.log(3), 99.], [0., 0., 99.]]], dtype=f.dtype)
    v = torch.tensor([[True, True, False]])
    z, w = m.compact_visual_tokens(f, l, v)
    torch.testing.assert_close(z, torch.tensor([[[2.5, 1.5], [2., 1.]]], dtype=f.dtype))
    torch.testing.assert_close(w, torch.tensor([[[.25, .75, 0.], [.5, .5, 0.]]], dtype=f.dtype))


def independent_images(m):
    f = torch.tensor([[[2.]], [[-4.]]])
    z, w = m.compact_visual_tokens(f, torch.tensor([[[1000.]], [[-1000.]]]))
    torch.testing.assert_close(z, f)
    torch.testing.assert_close(w, torch.ones((2, 1, 1)))
    assert z.dtype == w.dtype == f.dtype
    assert z.data_ptr() != f.data_ptr()


def stable_shift(m):
    f = torch.tensor([[[2., -1.], [4., 7.], [8., 3.]]], dtype=torch.float64)
    logits = torch.tensor([[[1., -1., 0.], [-3., 2., 4.]]], dtype=f.dtype)
    a, aw = m.compact_visual_tokens(f, logits)
    b, bw = m.compact_visual_tokens(f, logits + 9000)
    torch.testing.assert_close(a, b)
    torch.testing.assert_close(aw, bw)
    torch.testing.assert_close(bw.sum(-1), torch.ones((1, 2), dtype=f.dtype))
    assert torch.isfinite(b).all() and (bw >= 0).all()


def noncontiguous_and_immutable(m):
    f = torch.arange(24., dtype=torch.float64).reshape(2, 3, 4).transpose(1, 2)
    logits = torch.arange(16., dtype=f.dtype).reshape(2, 4, 2).transpose(1, 2)
    valid = torch.tensor([[True, True], [False, True], [True, False], [True, True]]).t()
    copies = [x.clone() for x in (f, logits, valid)]
    a, w = m.compact_visual_tokens(f, logits, valid)
    b, v = m.compact_visual_tokens(f.contiguous(), logits.contiguous(), valid.contiguous())
    torch.testing.assert_close(a, b); torch.testing.assert_close(w, v)
    for actual, copy in zip((f, logits, valid), copies):
        torch.testing.assert_close(actual, copy)
    assert a.data_ptr() not in (f.data_ptr(), logits.data_ptr(), w.data_ptr())
    assert w.data_ptr() not in (f.data_ptr(), logits.data_ptr())


def gradients(m):
    f = torch.tensor([[[1., 2.], [3., -1.], [5., 6.]]], dtype=torch.float64, requires_grad=True)
    logits = torch.tensor([[[.3, -.2, .9]]], dtype=f.dtype, requires_grad=True)
    valid = torch.tensor([[True, True, False]])
    assert torch.autograd.gradcheck(lambda a, b: m.compact_visual_tokens(a, b, valid), (f, logits))
    z, w = m.compact_visual_tokens(f, logits, valid)
    z.sum().backward()
    assert torch.equal(f.grad[:, 2], torch.zeros_like(f.grad[:, 2]))
    assert torch.equal(logits.grad[:, :, 2], torch.zeros_like(logits.grad[:, :, 2]))
    assert torch.equal(w[:, :, 2], torch.zeros_like(w[:, :, 2]))


def expect(error, fn):
    try:
        fn()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def invalid_types(m):
    f, l = torch.zeros((1, 2, 3)), torch.zeros((1, 1, 2))
    expect(TypeError, lambda: m.compact_visual_tokens(f.tolist(), l))
    expect(TypeError, lambda: m.compact_visual_tokens(f, l.tolist()))
    expect(TypeError, lambda: m.compact_visual_tokens(f, l, [[True, True]]))


def invalid_contracts(m):
    f, l = torch.zeros((1, 2, 3)), torch.zeros((1, 1, 2))
    for bad in (f.double(), f.long(), f[:, :0], f[0], torch.full_like(f, float("nan")), torch.full_like(f, 1e6 + 1)):
        expect(ValueError, lambda bad=bad: m.compact_visual_tokens(bad, l))
    for bad in (l.double(), l.long(), l[:, :, :1], l.repeat(1, 3, 1), torch.full_like(l, 10001.), torch.full_like(l, float("inf"))):
        expect(ValueError, lambda bad=bad: m.compact_visual_tokens(f, bad))
    for bad in (torch.zeros((1, 2), dtype=torch.bool), torch.ones((1, 2)), torch.ones((2,), dtype=torch.bool)):
        expect(ValueError, lambda bad=bad: m.compact_visual_tokens(f, l, bad))
    masked_nan = l.clone(); masked_nan[0, 0, 1] = float("nan")
    expect(ValueError, lambda: m.compact_visual_tokens(f, masked_nan, torch.tensor([[True, False]])))
    expect(ValueError, lambda: m.compact_visual_tokens(torch.zeros((17, 2, 1)), torch.zeros((17, 1, 2))))
    expect(ValueError, lambda: m.compact_visual_tokens(torch.zeros((2, 4096, 256)), torch.zeros((2, 1, 4096))))


def scale(m):
    gen = torch.Generator().manual_seed(20261113)
    f = torch.randn((4, 512, 32), generator=gen)
    l = torch.zeros((4, 8, 512))
    z, w = m.compact_visual_tokens(f, l)
    torch.testing.assert_close(z, f.mean(1)[:, None, :].expand(-1, 8, -1), atol=1e-6, rtol=1e-6)
    torch.testing.assert_close(w, torch.full_like(w, 1 / 512))


TESTS = [
    ("Masked weighted tokens", "public", example),
    ("Independent images", "public", independent_images),
    ("Stable logit shifts", "hidden", stable_shift),
    ("Noncontiguous inputs and fresh outputs", "hidden", noncontiguous_and_immutable),
    ("Autograd and zero masked influence", "hidden", gradients),
    ("Argument types", "hidden", invalid_types),
    ("Shape, value and validity contracts", "hidden", invalid_contracts),
    ("Larger feature maps", "hidden", scale),
]
