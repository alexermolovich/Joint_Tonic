import math
import torch


def reconstruction_example(m):
    p = torch.tensor([[[1., 3.], [100., 100.]]], dtype=torch.float64)
    t = torch.tensor([[[0., 1.], [0., 0.]]], dtype=p.dtype)
    values = m.cvae_loss(p, t, torch.tensor([[True, False]]), torch.tensor([[1., 0.]], dtype=p.dtype), torch.zeros((1, 2), dtype=p.dtype), 2)
    for actual, expected in zip(values, (2.5, 1.5, .5)):
        assert actual.shape == () and actual.dtype == p.dtype
        torch.testing.assert_close(actual, torch.tensor(expected, dtype=p.dtype))


def variance_example(m):
    p = torch.tensor([[[0.]], [[2.]]], dtype=torch.float64)
    values = m.cvae_loss(p, torch.zeros_like(p), torch.ones((2, 1), dtype=torch.bool), torch.zeros((2, 1), dtype=p.dtype), torch.tensor([[math.log(4)], [0.]], dtype=p.dtype), 1)
    kl = (3 - math.log(4)) / 4
    for actual, expected in zip(values, (1 + kl, 1, kl)):
        torch.testing.assert_close(actual, torch.tensor(expected, dtype=p.dtype))


def reductions(m):
    p = torch.tensor([[[2.], [0.]], [[0.], [0.]]])
    mean = torch.tensor([[0., 0.], [2., 0.]])
    total, reconstruction, kl = m.cvae_loss(p, torch.zeros_like(p), torch.tensor([[True, False], [False, False]]), mean, torch.zeros_like(mean), 3)
    torch.testing.assert_close(reconstruction, torch.tensor(2.))
    torch.testing.assert_close(kl, torch.tensor(1.))
    torch.testing.assert_close(total, torch.tensor(5.))


def gradients(m):
    p = torch.tensor([[[.5, -.7], [.9, .2]]], dtype=torch.float64, requires_grad=True)
    t = torch.tensor([[[.1, -.2], [-.1, .8]]], dtype=p.dtype, requires_grad=True)
    mu = torch.tensor([[.3, -.4]], dtype=p.dtype, requires_grad=True)
    lv = torch.tensor([[.2, -.5]], dtype=p.dtype, requires_grad=True)
    valid = torch.tensor([[True, False]])
    assert torch.autograd.gradcheck(lambda a,b,c,d: m.cvae_loss(a,b,valid,c,d,.7), (p,t,mu,lv))
    m.cvae_loss(p,t,valid,mu,lv,.7)[0].backward()
    torch.testing.assert_close(p.grad, -t.grad)
    assert torch.equal(p.grad[:,1], torch.zeros_like(p.grad[:,1]))
    zero = torch.zeros((1,1,1), requires_grad=True)
    m.cvae_loss(zero, torch.zeros_like(zero), torch.ones((1,1),dtype=torch.bool), torch.zeros((1,1)), torch.zeros((1,1)), 0)[0].backward()
    assert zero.grad.item() == 0


def layout_and_scale(m):
    p = torch.ones((8, 16, 64), dtype=torch.float32).transpose(1,2)
    t = torch.zeros_like(p); mu = torch.ones((8, 32))[:,::2]; lv = torch.zeros_like(mu)
    valid = torch.ones((64,8),dtype=torch.bool).t()
    before = [x.clone() for x in (p,t,mu,lv,valid)]
    total, r, kl = m.cvae_loss(p,t,valid,mu,lv,.5)
    torch.testing.assert_close(r,torch.tensor(1.)); torch.testing.assert_close(kl,torch.tensor(8.))
    torch.testing.assert_close(total,torch.tensor(5.))
    for x,y in zip((p,t,mu,lv,valid),before): torch.testing.assert_close(x,y)
    assert len({x.data_ptr() for x in (total,r,kl)}) == 3


def expect(error, fn):
    try: fn()
    except error: return
    raise AssertionError("expected "+error.__name__)


def validation(m):
    p=torch.zeros((1,2,1)); t=p.clone(); v=torch.tensor([[True,False]]); mu=torch.zeros((1,2)); lv=mu.clone()
    args=[p,t,v,mu,lv,1]
    for i in range(5):
        bad=args.copy(); bad[i]=bad[i].tolist()
        expect(TypeError,lambda bad=bad:m.cvae_loss(*bad))
    for beta in (True,"1",torch.tensor(1.)):
        expect(TypeError,lambda beta=beta:m.cvae_loss(p,t,v,mu,lv,beta))
    for beta in (-1,101,10**1000,float("nan")):
        expect(ValueError,lambda beta=beta:m.cvae_loss(p,t,v,mu,lv,beta))
    for i,badval in [(0,p.long()),(1,t.double()),(2,v.float()),(2,torch.zeros_like(v)),(3,torch.zeros((2,2))),(3,torch.full_like(mu,1001)),(4,torch.full_like(lv,21)),(4,torch.full_like(lv,-21)),(0,torch.full_like(p,float("nan")))]:
        bad=args.copy();bad[i]=badval
        expect(ValueError,lambda bad=bad:m.cvae_loss(*bad))


TESTS=[("Masked reconstruction plus KL","public",reconstruction_example),("Log variance and batch reduction","public",variance_example),
       ("KL includes empty-action batch items","hidden",reductions),("All four floating gradient paths","hidden",gradients),
       ("Layout scale and fresh scalars","hidden",layout_and_scale),("Typed bounded contract","hidden",validation)]
