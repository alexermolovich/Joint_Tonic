import torch


def affine(m):
    f=torch.tensor([[[1.,2.],[3.,4.]]],dtype=torch.float64)
    w=torch.tensor([[1.,0.,-1.],[0.,2.,1.]],dtype=f.dtype)
    b=torch.tensor([.5,-1.,2.],dtype=f.dtype)
    y=m.project_sensor_features(f,w,b,torch.tensor([[True,True]]))
    torch.testing.assert_close(y,torch.tensor([[[1.5,3.,3.],[3.5,7.,3.]]],dtype=f.dtype))


def masked_bias(m):
    y=m.project_sensor_features(torch.tensor([[[2.],[-5.]]]),torch.tensor([[3.,4.]]),torch.tensor([1.,-1.]),torch.tensor([[True,False]]))
    torch.testing.assert_close(y,torch.tensor([[[7.,7.],[0.,0.]]]))
    assert y.dtype == torch.float32


def empty_and_masked(m):
    f=torch.empty((2,0,3),dtype=torch.float64);w=torch.ones((3,4),dtype=f.dtype);b=torch.ones(4,dtype=f.dtype)
    y=m.project_sensor_features(f,w,b,torch.empty((2,0),dtype=torch.bool))
    assert y.shape == (2,0,4) and y.dtype == f.dtype
    y=m.project_sensor_features(torch.ones((2,3,3),dtype=f.dtype),w,b,torch.zeros((2,3),dtype=torch.bool))
    assert torch.equal(y,torch.zeros_like(y))


def gradients(m):
    f=torch.tensor([[[.2,.3],[-.5,.7]]],dtype=torch.float64,requires_grad=True)
    w=torch.tensor([[.4,-.2],[.3,.1]],dtype=f.dtype,requires_grad=True)
    b=torch.tensor([.1,-.4],dtype=f.dtype,requires_grad=True);v=torch.tensor([[True,False]])
    assert torch.autograd.gradcheck(lambda a,ww,bb:m.project_sensor_features(a,ww,bb,v),(f,w,b))
    m.project_sensor_features(f,w,b,v).sum().backward()
    assert torch.equal(f.grad[:,1],torch.zeros_like(f.grad[:,1]))
    torch.testing.assert_close(b.grad,torch.ones_like(b))


def layout_and_scale(m):
    f=torch.arange(256.,dtype=torch.float64).reshape(2,8,16).transpose(1,2)
    w=torch.ones((4,8),dtype=f.dtype).t(); b=torch.arange(8.,dtype=f.dtype)[::2]
    v=torch.ones((16,2),dtype=torch.bool).t()
    before=[x.clone() for x in (f,w,b,v)]
    y=m.project_sensor_features(f,w,b,v)
    torch.testing.assert_close(y,f.sum(-1,keepdim=True)+b)
    assert y.data_ptr() not in (f.data_ptr(),w.data_ptr(),b.data_ptr())
    for x,c in zip((f,w,b,v),before):torch.testing.assert_close(x,c)


def expect(error,fn):
    try:fn()
    except error:return
    raise AssertionError("expected "+error.__name__)


def contracts(m):
    f=torch.zeros((1,2,3));w=torch.zeros((3,4));b=torch.zeros(4);v=torch.ones((1,2),dtype=torch.bool)
    args=[f,w,b,v]
    for i in range(4):
        bad=args.copy();bad[i]=bad[i].tolist()
        expect(TypeError,lambda bad=bad:m.project_sensor_features(*bad))
    for i,val in [(0,f.long()),(1,w.double()),(1,w.t()),(2,b[:3]),(3,v.float()),(0,torch.full_like(f,float("nan"))),(2,torch.full_like(b,1001)),(0,f[0])]:
        bad=args.copy();bad[i]=val
        expect(ValueError,lambda bad=bad:m.project_sensor_features(*bad))
    expect(ValueError,lambda:m.project_sensor_features(torch.zeros((32,1024,1)),torch.zeros((1,512)),torch.zeros(512),torch.ones((32,1024),dtype=torch.bool)))


TESTS=[("Affine projection","public",affine),("Mask includes the bias","public",masked_bias),("Empty and missing tokens","hidden",empty_and_masked),
       ("Projection and mask gradients","hidden",gradients),("Noncontiguous layout and storage","hidden",layout_and_scale),("Input and output bounds","hidden",contracts)]
