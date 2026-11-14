import math
import numpy as np
import torch


def invalid(call,error=ValueError):
    try: call()
    except error: return
    raise AssertionError("Expected "+error.__name__)


def fixture(dtype=torch.float64,patches=1,views=2):
    return [torch.zeros((1,views,2),dtype=dtype),
            torch.tensor([[[1.,0.],[0.,1.]]],dtype=dtype),
            torch.zeros((1,patches,2),dtype=dtype),
            torch.full((1,patches,2),.5,dtype=dtype),
            torch.ones((1,patches),dtype=torch.bool)]


def checked(m,args,params,wanted):
    before=[x.detach().clone() for x in args]
    out=m.class_patch_loss(*args,*params)
    assert isinstance(out,torch.Tensor) and out.shape==() and out.dtype==args[0].dtype and out.device.type=="cpu"
    torch.testing.assert_close(out,torch.tensor(wanted,dtype=out.dtype),rtol=1e-6,atol=1e-7)
    assert all(torch.equal(x,saved) for x,saved in zip(args,before))
    return out


def weighted_example(m):
    args=fixture()
    args[2][0,0,0]=math.log(3)
    args[3][0,0]=torch.tensor([1.,0.])
    checked(m,args,(1.,1.,2.),math.log(2)+2*math.log(4/3))


def local_view_empty_selection(m):
    args=fixture(views=3)
    args[4][:]=False
    for x in args[:4]: x.requires_grad_()
    out=checked(m,args,(1.,2.,5.),2*math.log(2))
    out.backward()
    assert args[2].grad is not None and torch.equal(args[2].grad,torch.zeros_like(args[2]))
    assert args[1].grad is None and args[3].grad is None


def empty_patch_axis(m):
    for dtype in (torch.float32,torch.float64):
        args=fixture(dtype,patches=0)
        args[0].requires_grad_();args[2].requires_grad_()
        out=checked(m,args,(.2,1.,1.),math.log(2));out.backward()
        assert args[2].grad is not None and args[2].grad.shape==(1,0,2)


def independent_values_gradients(m):
    rng=np.random.default_rng(21);b,v,k,p=2,4,3,3;t=.7;cw=.4;pw=1.7
    arrays=[rng.normal(size=(b,v,k)),rng.uniform(.1,1.,(b,2,k)),
            rng.normal(size=(b,p,k)),rng.uniform(.1,1.,(b,p,k))]
    for i in (1,3): arrays[i]/=arrays[i].sum(axis=-1,keepdims=True)
    selected=np.array([[True,False,False],[True,True,False]])
    args=[torch.tensor(a,dtype=torch.float64,requires_grad=True) for a in arrays]+[torch.tensor(selected)]
    def probability(x):
        z=x/t;z-=z.max(axis=-1,keepdims=True);e=np.exp(z);return e/e.sum(axis=-1,keepdims=True)
    cs,ps=probability(arrays[0]),probability(arrays[2])
    class_grad=np.zeros_like(arrays[0]);patch_grad=np.zeros_like(arrays[2]);class_loss=0.
    for bi in range(b):
        for ti in range(2):
            for vi in range(v):
                if ti!=vi:
                    class_loss-=sum(arrays[1][bi,ti,ki]*math.log(cs[bi,vi,ki]) for ki in range(k))/(b*2*(v-1))
                    class_grad[bi,vi]+=(cs[bi,vi]-arrays[1][bi,ti])*cw/(b*2*(v-1)*t)
    patch_loss=0.;n=int(selected.sum())
    for bi,pi in zip(*np.nonzero(selected)):
        patch_loss-=sum(arrays[3][bi,pi,ki]*math.log(ps[bi,pi,ki]) for ki in range(k))/n
        patch_grad[bi,pi]=(ps[bi,pi]-arrays[3][bi,pi])*pw/(n*t)
    out=checked(m,args,(t,cw,pw),cw*class_loss+pw*patch_loss);out.backward()
    np.testing.assert_allclose(args[0].grad.numpy(),class_grad,rtol=1e-6,atol=1e-7)
    np.testing.assert_allclose(args[2].grad.numpy(),patch_grad,rtol=1e-6,atol=1e-7)
    assert args[1].grad is None and args[3].grad is None


def noncontiguous_zero_weights(m):
    args=fixture()
    args[0]=torch.zeros((1,4,4),dtype=torch.float64)[:,::2,::2].detach().requires_grad_()
    args[2]=torch.zeros((1,2,4),dtype=torch.float64)[:,::2,::2].detach().requires_grad_()
    assert not args[0].is_contiguous()
    checked(m,args,(.01,0.,0.),0.).backward()
    assert torch.equal(args[0].grad,torch.zeros_like(args[0]))
    assert torch.equal(args[2].grad,torch.zeros_like(args[2]))


def malformed(m):
    good=fixture()
    bad=good.copy();bad[0]=good[0].tolist()
    invalid(lambda:m.class_patch_loss(*bad,1,1,1),TypeError)
    replacements=[(0,good[0].long()),(0,torch.zeros((1,1,2),dtype=torch.float64)),
                  (0,torch.zeros((0,2,2),dtype=torch.float64)),(0,torch.zeros((1,2,1),dtype=torch.float64)),
                  (1,good[1].float()),(1,torch.ones_like(good[1])),(1,torch.full_like(good[1],-.5)),
                  (2,torch.zeros((1,1,3),dtype=torch.float64)),(3,torch.full_like(good[3],float("nan"))),
                  (0,torch.full_like(good[0],101)),(2,torch.full_like(good[2],float("inf"))),
                  (4,good[4].long()),(4,torch.ones((1,2),dtype=torch.bool)),
                  (0,torch.empty((1,2,2),device="meta"))]
    for index,value in replacements:
        bad=good.copy();bad[index]=value
        invalid(lambda:m.class_patch_loss(*bad,1,1,1))
    for params in [(True,1,1),(.001,1,1),(11,1,1),(1,-1,1),(1,1,11),(1,1,10**1000),(1,np.nan,1)]:
        invalid(lambda:m.class_patch_loss(*good,*params))
    bad=fixture();bad[4][:]=False;bad[3][:]=0
    invalid(lambda:m.class_patch_loss(*bad,1,1,1))


def realistic(m):
    b,v,k,p=8,6,128,64
    args=[torch.zeros((b,v,k)),torch.full((b,2,k),1/k),
          torch.zeros((b,p,k)),torch.full((b,p,k),1/k),
          torch.arange(p).expand(b,p)%2==0]
    checked(m,args,(.1,1.,1.),2*math.log(k))


TESTS=[
 ("Weighted class and patch example","public",weighted_example),
 ("Local crops without selected patches","public",local_view_empty_selection),
 ("Empty patch axis remains differentiable","public",empty_patch_axis),
 ("Independent values student gradients and teacher stop","hidden",independent_values_gradients),
 ("Strided inputs and zero weights","hidden",noncontiguous_zero_weights),
 ("Malformed objectives and unselected target validation","hidden",malformed),
 ("Larger cross-view batch","hidden",realistic),
]

