import numpy as np
import math,copy
from numpy.testing import assert_allclose,assert_array_equal

def f(x):return np.array(x,dtype=np.float64)
def args():return [np.ones((1,1,1)),np.ones((1,1)),np.full((1,3),.5),np.ones((1,1,1)),np.ones((1,1)),np.full((1,3),.5),np.full(3,.5),np.zeros((1,4)),np.zeros(4),3,.1]
def eq(a,b):
    if isinstance(b,dict):
        assert isinstance(a,dict) and a.keys()==b.keys()
        for k in b:eq(a[k],b[k])
    elif isinstance(b,np.ndarray):
        assert isinstance(a,np.ndarray) and a.shape==b.shape and a.dtype==np.float64
        assert_allclose(a,b,rtol=1e-6,atol=1e-7)
    else:assert type(a) is type(b);assert_allclose(a,b,rtol=1e-6,atol=1e-7)
def checked(m,a):
    before=copy.deepcopy(a);out=m.train_tiny_field(*a)
    for x,y in zip(before,a):
        if isinstance(x,np.ndarray):assert_array_equal(x,y)
        else:assert x==y
    arrays=[v for v in out.values() if isinstance(v,np.ndarray)]
    for x in arrays:
        for y in a:
            if isinstance(y,np.ndarray):assert not np.shares_memory(x,y)
        for y in arrays:
            if y is not x:assert not np.shares_memory(x,y)
    return out
def example1(m):
    eq(checked(m,args()),dict(weight=np.zeros((1,4)),bias=np.zeros(4),train_loss=np.zeros(4),gradient_norm=np.zeros(3),eval_rgb=np.full((1,3),.5),eval_mse=0.))
def example2(m):
    a=args();a[2][:]=0;a[5][:]=0;a[6][:]=0;a[-2]=1
    row=f([-1/160,-1/480,-1/480,-1/480]);value=(1-math.exp(-math.log1p(math.exp(-1/80))))/(1+math.exp(1/240))
    eq(checked(m,a),dict(weight=row[None].copy(),bias=row.copy(),train_loss=f([1/16,value**2]),gradient_norm=f([math.sqrt(1/96)]),eval_rgb=np.full((1,3),value),eval_mse=float(value**2)))

def scalar_render(x,intervals,bg,w,bias):
    output=[]
    for ray in range(x.shape[0]):
        remaining=1.;color=np.zeros(3)
        for s in range(x.shape[1]):
            raw=[sum(float(x[ray,s,j])*w[j,k] for j in range(x.shape[2]))+bias[k] for k in range(4)]
            density=math.log1p(math.exp(raw[0]));rgb=f([1/(1+math.exp(-v)) for v in raw[1:]])
            survival=math.exp(-density*intervals[ray,s]);color+=remaining*(1-survival)*rgb;remaining*=survival
        output.append(color+remaining*bg)
    return f(output)
def scalar_loss(a,w,bias):return float(np.mean((scalar_render(a[0],a[1],a[6],w,bias)-a[2])**2))
def numerical_gradients(a):
    w=a[7];bias=a[8];gw=np.zeros_like(w);gb=np.zeros_like(bias);eps=1e-5
    for idx in np.ndindex(w.shape):
        plus=w.copy();minus=w.copy();plus[idx]+=eps;minus[idx]-=eps
        gw[idx]=(scalar_loss(a,plus,bias)-scalar_loss(a,minus,bias))/(2*eps)
    for j in range(4):
        plus=bias.copy();minus=bias.copy();plus[j]+=eps;minus[j]-=eps
        gb[j]=(scalar_loss(a,w,plus)-scalar_loss(a,w,minus))/(2*eps)
    return gw,gb
def gradient_oracle(m):
    rng=np.random.default_rng(1013)
    a=[rng.uniform(-1,1,(2,3,4))[:,:,::2],rng.uniform(.1,1,(2,3)),rng.uniform(size=(2,3)),rng.uniform(-1,1,(3,3,2)),rng.uniform(.1,1,(3,3)),rng.uniform(size=(3,3)),f([.1,.4,.9]),rng.uniform(-.3,.3,(2,4)),rng.uniform(-.3,.3,4),1,.05]
    gw,gb=numerical_gradients(a);norm=float(np.linalg.norm(np.r_[gw.ravel(),gb]));w=a[7]-.05*gw/max(1,norm);bias=a[8]-.05*gb/max(1,norm);ev=scalar_render(a[3],a[4],a[6],w,bias)
    eq(checked(m,a),dict(weight=w,bias=bias,train_loss=f([scalar_loss(a,a[7],a[8]),scalar_loss(a,w,bias)]),gradient_norm=f([norm]),eval_rgb=ev,eval_mse=float(np.mean((ev-a[5])**2))))
def clipping_and_isolation(m):
    a=[np.full((1,1,16),2.),np.full((1,1),2.),np.ones((1,3)),np.full((1,1,16),2.),np.full((1,1),2.),np.ones((1,3)),np.zeros(3),np.zeros((16,4)),f([-2,2,2,2]),1,.1]
    gw,gb=numerical_gradients(a);norm=float(np.linalg.norm(np.r_[gw.ravel(),gb]));assert norm>1
    out=checked(m,a);eq(out['gradient_norm'],f([norm]));eq(out['weight'],a[7]-.1*gw/norm);eq(out['bias'],a[8]-.1*gb/norm)
    assert_allclose(np.linalg.norm(np.r_[(out['weight']-a[7]).ravel(),out['bias']-a[8]]),.1,rtol=1e-6)
    a[-2]=8;first=checked(m,a);a[3][:]=-.5;a[4][:]=.2;a[5][:]=0;second=checked(m,a)
    for key in ('weight','bias','train_loss','gradient_norm'):assert_array_equal(first[key],second[key])
    assert first['eval_mse']!=second['eval_mse']
def boundaries(m):
    a=args();a[-2]=0;a[2][:]=0;out=checked(m,a);assert out['gradient_norm'].shape==(0,);eq(out['weight'],a[7]);eq(out['bias'],a[8]);eq(out['train_loss'],f([.25]));eq(out['eval_rgb'],np.full((1,3),.5))
    a=[np.full((16,32,16),2.),np.full((16,32),.01),np.zeros((16,3)),np.full((16,32,16),-2.),np.full((16,32),2.),np.ones((16,3)),np.ones(3),np.full((16,4),2.),np.full(4,-2.),64,.1]
    out=checked(m,a);assert out['train_loss'].shape==(65,) and out['gradient_norm'].shape==(64,)
    assert all(np.isfinite(x).all() for x in out.values());assert np.all(out['eval_rgb']>=0) and np.all(out['eval_rgb']<=1)
def invalid(m):
    a=args()
    def reject(q):
        try:m.train_tiny_field(*q)
        except ValueError:return
        raise AssertionError('Expected ValueError')
    for index in range(9):
        for value in (a[index].astype(np.float32),a[index].tolist()):q=a.copy();q[index]=value;reject(q)
        q=copy.deepcopy(a);q[index].flat[0]=np.nan;reject(q)
    for index,value in [(0,np.zeros((1,0,1))),(3,np.zeros((1,2,1))),(4,f([[0]])),(5,f([[2,0,0]])),(7,f([[3,0,0,0]])),(9,True),(9,65),(10,0.),(10,float('inf')),(10,10**1000),(10,-10**1000)]:q=a.copy();q[index]=value;reject(q)

TESTS=[('Zero-error field','public',example1),('One analytic SGD step','public',example2),('Independent scalar renderer and finite-difference gradient','hidden',gradient_oracle),('Global clipping and held-out isolation','hidden',clipping_and_isolation),('Zero steps, maximum dimensions and stable arithmetic','hidden',boundaries),('Documented invalid inputs','hidden',invalid)]
