import torch


def close(x,y):torch.testing.assert_close(x,torch.as_tensor(y,dtype=x.dtype),rtol=1e-6,atol=1e-7)


def scaled(m):close(m.feature_transform_penalty(torch.tensor([[[2.,0.],[0.,1.]]],dtype=torch.float64)),9.)


def batch_mean(m):close(m.feature_transform_penalty(torch.tensor([[[1.,0.],[0.,1.]],[[2.,0.],[0.,1.]]])),4.5)


def reflection(m):close(m.feature_transform_penalty(torch.tensor([[[-1.,0.],[0.,1.]]])),0.)


def gradients(m):
    x=torch.tensor([[[2.,0.],[0.,1.]]],dtype=torch.float64,requires_grad=True)
    loss=m.feature_transform_penalty(x);g,=torch.autograd.grad(loss,x)
    close(g,[[[24,0],[0,0]]]);assert loss.ndim==0 and loss.dtype==x.dtype


def oracle_layout(m):
    g=torch.Generator().manual_seed(20261113)
    x=torch.randn((5,7,7),generator=g,dtype=torch.float64).transpose(1,2);old=x.clone()
    loss=m.feature_transform_penalty(x)
    expected=sum(sum((sum(float(x[b,i,k]*x[b,j,k]) for k in range(7))-(1 if i==j else 0))**2 for i in range(7) for j in range(7)) for b in range(5))/5
    close(loss,expected);close(x,old)


def invalid(m):
    def expect(kind,x):
        try:m.feature_transform_penalty(x)
        except kind:return
        raise AssertionError("Expected "+kind.__name__)
    expect(TypeError,[[[1]]])
    for x in [torch.ones((1,2,3)),torch.empty((0,2,2)),torch.ones((1,2,2),dtype=torch.int64),torch.full((1,2,2),float('nan')),torch.full((1,1,1),11.),torch.empty((1,2,2),device="meta")]:expect(ValueError,x)


TESTS=[("Scale residual","public",scaled),("Batch-only mean","public",batch_mean),("Reflection is orthogonal","public",reflection),
       ("Gradient path","hidden",gradients),("Independent matrix oracle","hidden",oracle_layout),("Validation","hidden",invalid)]
