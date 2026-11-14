import torch


def check(a, b):
    torch.testing.assert_close(a, torch.as_tensor(b, dtype=a.dtype), rtol=1e-6, atol=1e-7)


def rows(m):
    a = torch.tensor([[3.,4.],[0.,-2.]],dtype=torch.float64)
    b = torch.tensor([[0.,5.],[-8.,6.]],dtype=torch.float64)
    x,y = m.normalize_clip_embeddings(a,b)
    check(x,[[.6,.8],[0.,-1.]])
    check(y,[[0.,1.],[-.8,.6]])


def scaling(m):
    a = torch.tensor([[2.,0.,0.],[20.,0.,0.]])
    b = torch.tensor([[0.,0.,-7.],[0.,0.,-.5]])
    x,y = m.normalize_clip_embeddings(a,b)
    check(x,[[1.,0.,0.],[1.,0.,0.]])
    check(y,[[0.,0.,-1.],[0.,0.,-1.]])


def single_feature(m):
    a = torch.tensor([[-2.],[8.]])
    x,y = m.normalize_clip_embeddings(a,a)
    check(x,[[-1.],[1.]])
    check(y,x)


def gradient(m):
    a=torch.tensor([[3.,4.]],dtype=torch.float64,requires_grad=True)
    b=torch.tensor([[4.,3.]],dtype=torch.float64,requires_grad=True)
    x,y=m.normalize_clip_embeddings(a,b)
    ga,gb=torch.autograd.grad(x[0,0]+y[0,0],(a,b))
    check(ga,[[.128,-.096]])
    check(gb,[[.072,-.096]])


def layout_storage(m):
    a=torch.arange(1.,25.,dtype=torch.float64).reshape(4,6).T
    b=-a.clone()
    old=a.clone()
    x,y=m.normalize_clip_embeddings(a,b)
    check(torch.linalg.vector_norm(x,dim=1),torch.ones(6))
    check(y,-x)
    assert x.data_ptr()!=a.data_ptr() and y.data_ptr()!=b.data_ptr()
    check(a,old)
    assert x.dtype==a.dtype and x.device==a.device


def invalid(m):
    def expect(kind,a,b):
        try: m.normalize_clip_embeddings(a,b)
        except kind: return
        raise AssertionError("Expected "+kind.__name__)
    good=torch.ones((2,3),dtype=torch.float64)
    expect(TypeError,[[1.]],good)
    for x in [torch.zeros_like(good),torch.full_like(good,float('nan')),torch.full_like(good,1e7),torch.full_like(good,1e-9),torch.ones((0,3),dtype=torch.float64),torch.ones(3,dtype=torch.float64),torch.ones((2,3),dtype=torch.int64),torch.ones((2,4),dtype=torch.float64),good.float()]:
        expect(ValueError,x,good)
    expect(ValueError,torch.empty((2,3),device="meta"),good)


def boundary(m):
    a=torch.tensor([[1e-6,0.],[1e6,0.]],dtype=torch.float64)
    x,y=m.normalize_clip_embeddings(a,a)
    check(x,[[1.,0.],[1.,0.]])
    check(y,x)


def scale(m):
    g=torch.Generator().manual_seed(20261113)
    a=torch.randn((512,512),generator=g)
    b=torch.randn((512,512),generator=g)
    x,y=m.normalize_clip_embeddings(a,b)
    check(torch.linalg.vector_norm(x,dim=1),torch.ones(512))
    check(torch.linalg.vector_norm(y,dim=1),torch.ones(512))


TESTS=[("Independent rows","public",rows),("Positive rescaling","public",scaling),("One feature","public",single_feature),
       ("Gradient connection","hidden",gradient),("Layout and storage","hidden",layout_storage),("Validation","hidden",invalid),
       ("Norm boundaries","hidden",boundary),("Realistic batch","hidden",scale)]
