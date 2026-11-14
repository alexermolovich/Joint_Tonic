import torch

def expect(kind,fn):
    try: fn()
    except kind: return
    raise AssertionError('expected '+kind.__name__)

def example1(m):
    y,v=m.fuse_visual_features(torch.tensor([[[1.,2.],[8.,9.]]],dtype=torch.float64),torch.tensor([[[3.],[4.]]],dtype=torch.float64),torch.tensor([[1.,0.],[0.,1.],[2.,-1.]],dtype=torch.float64),torch.tensor([.5,1.],dtype=torch.float64),torch.tensor([[True,True]]),torch.tensor([[True,False]]))
    torch.testing.assert_close(y,torch.tensor([[[7.5,0.],[0.,0.]]],dtype=torch.float64));assert torch.equal(v,torch.tensor([[True,False]]))

def example2(m):
    y,v=m.fuse_visual_features(torch.tensor([[[2.]]]),torch.tensor([[[5.]]]),torch.tensor([[1.],[10.]]),torch.zeros(1),torch.ones((1,1),dtype=torch.bool),torch.ones((1,1),dtype=torch.bool))
    torch.testing.assert_close(y,torch.tensor([[[52.]]]));assert v.dtype==torch.bool

def gradients_and_masks(m):
    f=torch.tensor([[[1.],[3.],[5.]]],dtype=torch.float64,requires_grad=True);s=torch.tensor([[[2.],[4.],[6.]]],dtype=torch.float64,requires_grad=True)
    w=torch.tensor([[2.],[3.]],dtype=torch.float64,requires_grad=True);b=torch.tensor([1.],dtype=torch.float64,requires_grad=True)
    ma=torch.tensor([[True,False,True]]);mb=torch.tensor([[True,True,False]])
    y,v=m.fuse_visual_features(f,s,w,b,ma,mb);y.sum().backward()
    torch.testing.assert_close(y,torch.tensor([[[9.],[0.],[0.]]],dtype=torch.float64));assert torch.equal(v,torch.tensor([[True,False,False]]))
    torch.testing.assert_close(f.grad,torch.tensor([[[2.],[0.],[0.]]],dtype=torch.float64));torch.testing.assert_close(s.grad,torch.tensor([[[3.],[0.],[0.]]],dtype=torch.float64))
    torch.testing.assert_close(w.grad,torch.tensor([[1.],[2.]],dtype=torch.float64));torch.testing.assert_close(b.grad,torch.ones(1,dtype=torch.float64))
    for a in [f,s,w,b]:a.grad=None
    m.fuse_visual_features(f,s,w,b,torch.zeros_like(ma),mb)[0].sum().backward()
    for a in [f,s,w,b]:assert a.grad is not None and torch.count_nonzero(a.grad)==0

def noncontiguous_scale(m):
    for dtype in [torch.float32,torch.float64]:
        f=torch.arange(48,dtype=dtype).reshape(2,6,4).transpose(1,2);s=(f+1)[:,:,:2];w=torch.ones((5,8),dtype=dtype).T;b=torch.arange(10,dtype=dtype)[::2];mask=torch.ones((4,2),dtype=torch.bool).T
        args=[f,s,w,b,mask,mask];copies=[x.clone() for x in args];y,v=m.fuse_visual_features(*args)
        torch.testing.assert_close(y,(f.sum(-1)+s.sum(-1))[...,None]+b)
        assert y.dtype==dtype and y.data_ptr() not in [x.data_ptr() for x in args] and v.data_ptr()!=mask.data_ptr()
        for x,c in zip(args,copies):torch.testing.assert_close(x,c)
    f=torch.ones((32,128,16));s=torch.ones((32,128,16));w=torch.ones((32,32));b=torch.zeros(32);mask=torch.ones((32,128),dtype=torch.bool)
    y,v=m.fuse_visual_features(f,s,w,b,mask,mask);assert y.shape==(32,128,32);assert torch.all(y==32)

def invalid(m):
    args=[torch.zeros((1,2,3)),torch.zeros((1,2,2)),torch.zeros((5,4)),torch.zeros(4),torch.ones((1,2),dtype=torch.bool),torch.ones((1,2),dtype=torch.bool)]
    for i in range(6):
        a=args.copy();a[i]=a[i].tolist();expect(TypeError,lambda a=a:m.fuse_visual_features(*a))
    for i,x in [(0,torch.zeros((1,0,3))),(1,torch.zeros((1,3,2))),(2,torch.zeros((4,4))),(3,torch.zeros((1,4))),(4,args[4].float()),(5,torch.ones((2,1),dtype=torch.bool)),(0,args[0].long()),(1,args[1].double()),(0,torch.full_like(args[0],float('nan'))),(2,torch.full_like(args[2],101.)),(3,torch.full_like(args[3],float('inf'))),(0,torch.zeros((1,2,3),device='meta'))]:
        a=args.copy();a[i]=x;expect(ValueError,lambda a=a:m.fuse_visual_features(*a))
    a=args.copy();a[0]=torch.full_like(args[0],float('nan'));a[4]=torch.zeros_like(args[4]);expect(ValueError,lambda:m.fuse_visual_features(*a))
    expect(ValueError,lambda:m.fuse_visual_features(torch.zeros((32,512,1)),torch.zeros((32,512,1)),torch.zeros((2,512)),torch.zeros(512),torch.ones((32,512),dtype=torch.bool),torch.ones((32,512),dtype=torch.bool)))

TESTS=[('Affine fused patches','public',example1),('Ordered feature concatenation','public',example2),('Intersection masks and gradients','hidden',gradients_and_masks),('Noncontiguous storage and scale','hidden',noncontiguous_scale),('Typed bounded inputs','hidden',invalid)]
