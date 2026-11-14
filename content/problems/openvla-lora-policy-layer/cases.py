import torch

def expect(kind,fn):
    try:fn()
    except kind:return
    raise AssertionError('expected '+kind.__name__)

def run_example(m,x,w,a,b,alpha,expected,dx):
    x,w,a,b=[torch.tensor(v,dtype=torch.float64,requires_grad=True) for v in [x,w,a,b]]
    y=m.lora_policy_linear(x,w,a,b,alpha);torch.testing.assert_close(y,torch.tensor(expected,dtype=torch.float64));y.sum().backward()
    assert w.grad is None and w.requires_grad
    torch.testing.assert_close(x.grad,torch.tensor(dx,dtype=torch.float64));return x,w,a,b

def example1(m):
    run_example(m,[[[1.,2.]]],[[1.,0.],[0.,1.]],[[1.,-1.]],[[2.],[3.]],2,[[[-3.,-4.]]],[[[11.,-9.]]])

def example2(m):
    _,_,a,b=run_example(m,[[[3.,4.]]],[[2.,0.],[0.,-1.]],[[1.,1.]],[[0.],[0.]],1,[[[6.,-4.]]],[[[2.,-1.]]])
    assert a.grad is not None and torch.count_nonzero(a.grad)==0;torch.testing.assert_close(b.grad,torch.full_like(b,7.))

def gradients_and_zero(m):
    x=torch.tensor([[[.2,.3]]],dtype=torch.float64,requires_grad=True);w=torch.tensor([[.4,.5],[.1,.2]],dtype=torch.float64,requires_grad=True);a=torch.tensor([[.6,.7],[.2,.3]],dtype=torch.float64,requires_grad=True);b=torch.tensor([[.8,.9],[.3,.4]],dtype=torch.float64,requires_grad=True)
    assert torch.autograd.gradcheck(lambda x,a,b:m.lora_policy_linear(x,w,a,b,3),(x,a,b))
    m.lora_policy_linear(x,w,a,b,0).sum().backward();assert w.grad is None
    torch.testing.assert_close(x.grad,w.detach().sum(0)[None,None,:])
    for v in [a,b]:assert v.grad is not None and torch.count_nonzero(v.grad)==0

def storage_rank_scale(m):
    for dtype in [torch.float32,torch.float64]:
        x=torch.arange(24,dtype=dtype).reshape(2,4,3).transpose(1,2)/10;w=torch.ones((4,3),dtype=dtype).T;a=torch.ones((4,2),dtype=dtype).T;b=torch.ones((2,3),dtype=dtype).T
        snapshots=[v.clone() for v in [x,w,a,b]];y=m.lora_policy_linear(x,w,a,b,4)
        expected=5*x.sum(-1,keepdim=True).expand(2,3,3);torch.testing.assert_close(y,expected)
        assert y.dtype==dtype and y.data_ptr() not in [v.data_ptr() for v in [x,w,a,b]]
        for v,c in zip([x,w,a,b],snapshots):torch.testing.assert_close(v,c)
    y=m.lora_policy_linear(torch.ones((16,64,32)),torch.ones((64,32)),torch.ones((8,32)),torch.ones((64,8)),8);assert y.shape==(16,64,64);assert torch.all(y==288)

def invalid(m):
    args=[torch.zeros((1,2,3)),torch.zeros((4,3)),torch.zeros((2,3)),torch.zeros((4,2)),2]
    for i in range(4):
        a=args.copy();a[i]=a[i].tolist();expect(TypeError,lambda a=a:m.lora_policy_linear(*a))
    for i,v in [(0,args[0].long()),(1,args[1].double()),(0,torch.zeros((1,0,3))),(0,torch.zeros((1,2,3),device='meta')),(1,torch.zeros((4,2))),(2,torch.zeros((4,3))),(3,torch.zeros((4,1))),(0,torch.full_like(args[0],11.)),(2,torch.full_like(args[2],float('nan'))),(3,torch.full_like(args[3],float('inf')))]:
        a=args.copy();a[i]=v;expect(ValueError,lambda a=a:m.lora_policy_linear(*a))
    for v in [True,-1,65,10**1000,float('nan'),float('inf'),torch.tensor(2),[2],'2']:
        a=args.copy();a[-1]=v;expect(ValueError,lambda a=a:m.lora_policy_linear(*a))
    expect(ValueError,lambda:m.lora_policy_linear(torch.ones((32,256,1)),torch.ones((256,1)),torch.ones((1,1)),torch.ones((256,1)),1))

TESTS=[('Rank-one update with frozen base','public',example1),('Zero up-projection can still learn','public',example2),('Rank scaling and differentiable zero','hidden',gradients_and_zero),('Noncontiguous independent storage and scale','hidden',storage_rank_scale),('Typed bounded contract','hidden',invalid)]
