import math
import torch
import numpy as np


def invalid(call, error=ValueError):
    try:
        call()
    except error:
        return
    raise AssertionError("Expected " + error.__name__)


def cubic(distance):
    x=abs(distance)
    if x<=1:
        return 1.25*x**3-2.25*x**2+1
    if x<2:
        return -.75*x**3+3.75*x**2-6*x+3
    return 0.


def independent_matrix(old,new):
    h,w=old; hh,ww=new
    matrix=np.zeros((hh*ww,h*w))
    for r in range(hh):
        y=(r+.5)*h/hh-.5; j=math.floor(y)
        for c in range(ww):
            x=(c+.5)*w/ww-.5; i=math.floor(x)
            for yy in range(j-1,j+3):
                for xx in range(i-1,i+3):
                    source=min(max(yy,0),h-1)*w+min(max(xx,0),w-1)
                    matrix[r*ww+c,source]+=cubic(y-yy)*cubic(x-xx)
    return matrix


def checked(m,p,old,new,expected):
    before=p.detach().clone()
    out=m.resize_positions(p,old,new)
    assert isinstance(out,torch.Tensor) and out.dtype==p.dtype and out.device==p.device
    assert out.shape==(1,1+new[0]*new[1],p.shape[-1])
    torch.testing.assert_close(out,expected,rtol=1e-6,atol=1e-7)
    assert torch.equal(out[:,:1,:],p[:,:1,:]) and torch.equal(p,before)
    assert out.untyped_storage().data_ptr()!=p.untyped_storage().data_ptr()
    return out


def symmetric_mean(m):
    p=torch.tensor([[[99.],[1.],[2.],[3.],[4.]]],dtype=torch.float64)
    checked(m,p,(2,2),(1,1),torch.tensor([[[99.],[2.5]]],dtype=torch.float64))


def constant_field(m):
    p=torch.tensor([[[7.,8.],[2.,3.],[2.,3.]]],dtype=torch.float32)
    expected=torch.tensor([[[7.,8.]]+[[2.,3.]]*6],dtype=torch.float32)
    checked(m,p,(1,2),(2,3),expected)


def identity(m):
    for dtype in (torch.float32,torch.float64):
        p=torch.arange(20,dtype=dtype).reshape(1,5,4)
        checked(m,p,(2,2),(2,2),p.clone())


def independent_values_gradients(m):
    p=torch.arange(28,dtype=torch.float64).reshape(1,7,4).requires_grad_()
    weights=independent_matrix((2,3),(4,2))
    expected=torch.cat((p.detach()[:,:1],torch.from_numpy(weights@p.detach().numpy()[0,1:])[None]),dim=1)
    out=checked(m,p,(2,3),(4,2),expected)
    out.sum().backward()
    wanted=np.concatenate((np.ones((1,4)),np.repeat(weights.sum(axis=0)[:,None],4,axis=1)),axis=0)[None]
    np.testing.assert_allclose(p.grad.numpy(),wanted,rtol=1e-6,atol=1e-7)


def noncontiguous(m):
    base=torch.linspace(-2,2,1*13*10,dtype=torch.float64).reshape(1,13,10)
    p=base[:,:,::2].detach().requires_grad_()
    assert not p.is_contiguous()
    weights=independent_matrix((3,4),(2,5))
    expected=torch.cat((p.detach()[:,:1],torch.from_numpy(weights@p.detach().numpy()[0,1:])[None]),dim=1)
    checked(m,p,(3,4),(2,5),expected).sum().backward()
    assert p.grad is not None and torch.isfinite(p.grad).all()


def malformed(m):
    p=torch.zeros((1,5,2),dtype=torch.float64)
    invalid(lambda:m.resize_positions(p.tolist(),(2,2),(1,1)),TypeError)
    for bad in [p.long(),p[0],p.repeat(2,1,1),p[:,:4],torch.zeros((1,5,0)),
                torch.full((1,5,2),float("nan")),torch.full((1,5,2),float("inf")),
                torch.full((1,5,2),101.),torch.empty((1,5,2),device="meta")]:
        invalid(lambda:m.resize_positions(bad,(2,2),(1,1)))
    for grid in [[2,2],(True,2),(0,2),(129,2),(2,), (np.int64(2),2)]:
        invalid(lambda:m.resize_positions(p,grid,(1,1)))
        invalid(lambda:m.resize_positions(p,(2,2),grid))
    invalid(lambda:m.resize_positions(torch.zeros((1,5,64)),(2,2),(128,128)))
    invalid(lambda:m.resize_positions(torch.zeros((1,5,257)),(2,2),(1,1)))


def realistic(m):
    p=torch.full((1,1+64*64,64),.25,dtype=torch.float32)
    p[:,0,:]=.75
    out=m.resize_positions(p,(64,64),(100,100))
    assert out.shape==(1,10001,64)
    torch.testing.assert_close(out[:,1:,:],torch.full((1,10000,64),.25),rtol=1e-6,atol=1e-7)
    assert torch.equal(out[:,0,:],p[:,0,:])


TESTS=[
 ("Class row outside spatial average","public",symmetric_mean),
 ("Constant rectangular spatial field","public",constant_field),
 ("Identity grid with independent storage","public",identity),
 ("Independent bicubic values and gradients","hidden",independent_values_gradients),
 ("Noncontiguous rectangular interpolation","hidden",noncontiguous),
 ("Malformed grids tensors and budgets","hidden",malformed),
 ("Bounded resolution transfer","hidden",realistic),
]

