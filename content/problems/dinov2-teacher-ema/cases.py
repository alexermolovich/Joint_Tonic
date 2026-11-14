import torch


def close(a,b):
    torch.testing.assert_close(a,torch.as_tensor(b,dtype=a.dtype),rtol=1e-6,atol=1e-7)


def named_update(m):
    t={'weight':torch.tensor([2.,4.],dtype=torch.float64),'bias':torch.tensor(1.,dtype=torch.float64)}
    s={'bias':torch.tensor(3.,dtype=torch.float64),'weight':torch.tensor([6.,0.],dtype=torch.float64)}
    y=m.update_teacher_ema(t,s,.9)
    assert list(y)==['weight','bias']
    close(y['weight'],[2.4,3.6]);close(y['bias'],1.2)


def endpoint(m):
    t={'w':torch.tensor([-1.,2.])};s={'w':torch.tensor([5.,7.],requires_grad=True)}
    y=m.update_teacher_ema(t,s,0)
    close(y['w'],[5,7]);assert not y['w'].requires_grad and y['w'].grad_fn is None
    y['w'][0]=100
    close(s['w'],[5,7])


def empty(m):
    assert m.update_teacher_ema({}, {},.5)=={}


def sequential(m):
    t={'w':torch.tensor([2.,4.],dtype=torch.float64)}
    s={'w':torch.tensor([6.,0.],dtype=torch.float64)}
    one=m.update_teacher_ema(t,s,.9)
    two=m.update_teacher_ema(one,{'w':torch.tensor([0.,8.],dtype=torch.float64)},.9)
    close(two['w'],[2.16,4.04])
    close(t['w'],[2,4]);close(s['w'],[6,0])


def mixed_shapes(m):
    t={'scalar':torch.tensor(3.,dtype=torch.float64,requires_grad=True),'empty':torch.empty((0,2)),'view':torch.arange(12.).reshape(3,4).T}
    s={k:torch.zeros_like(v) for k,v in t.items()}
    y=m.update_teacher_ema(t,s,1)
    for k,v in t.items():
        close(y[k],v)
        assert y[k].shape==v.shape and y[k].dtype==v.dtype and not y[k].requires_grad
        if v.numel():assert y[k].data_ptr()!=v.data_ptr()
    assert y is not t


def invalid(m):
    def expect(kind,t,s,mu=.5):
        try:m.update_teacher_ema(t,s,mu)
        except kind:return
        raise AssertionError("Expected "+kind.__name__)
    good={'w':torch.ones(2)}
    expect(TypeError,[],good);expect(TypeError,{'w':[1,2]},good)
    for mu in [True,-.1,1.1,float('nan'),10**1000]:expect(ValueError,good,good,mu)
    expect(ValueError,{'':torch.ones(2)},{'':torch.ones(2)})
    expect(ValueError,good,{'b':torch.ones(2)})
    for bad in [torch.ones(3),torch.ones(2,dtype=torch.float64),torch.ones(2,dtype=torch.int64),torch.tensor([float('inf'),1.]),torch.empty(2,device="meta")]:
        expect(ValueError,good,{'w':bad})


def scale(m):
    t={'w':torch.full((256,256),2.)};s={'w':torch.full((256,256),6.)}
    y=m.update_teacher_ema(t,s,.75)
    close(y['w'],torch.full((256,256),3.))


TESTS=[("Named parameter update","public",named_update),("Detached endpoint","public",endpoint),("Empty dictionaries","public",empty),
       ("Sequential training updates","hidden",sequential),("Shapes dtype and independent storage","hidden",mixed_shapes),
       ("Validation","hidden",invalid),("Parameter batch","hidden",scale)]
