import numpy as np, math
from numpy.testing import assert_allclose,assert_array_equal
def params(d=2,f=3):
    return dict(q=np.zeros((d,d)),k=np.zeros((d,d)),v=np.zeros((d,d)),o=np.zeros((d,d)),w1=np.zeros((d,f)),b1=np.zeros(f),w2=np.zeros((f,d)),b2=np.zeros(d),gamma=np.ones((2,d)),beta=np.zeros((2,d)))
def residual(m):
    x=np.array([[2.,4.],[7,-3]]);assert_allclose(m.vit_block(x,params()),x)
def bias(m):
    p=params();p['b2'][:]=[1,-1];assert_allclose(m.vit_block(np.array([[2.,4.]]),p),[[3,3]])
def oracle(m):
    rng=np.random.default_rng(12);x=rng.normal(size=(4,3));p=params(3,5)
    for k in p:p[k]=rng.normal(size=p[k].shape)
    def norm(a,j):
        rows=[]
        for row in a:
            mu=sum(row)/len(row);var=sum((z-mu)**2 for z in row)/len(row);rows.append([(z-mu)/(var+1e-5)**.5*p['gamma'][j,k]+p['beta'][j,k] for k,z in enumerate(row)])
        return np.array(rows)
    z=norm(x,0);q=z@p['q'];k=z@p['k'];v=z@p['v'];mix=[]
    for row in q:
        scores=np.array([sum(a*b for a,b in zip(row,key))/3**.5 for key in k]);weights=np.exp(scores-max(scores));weights/=sum(weights);mix.append(sum(w*vec for w,vec in zip(weights,v)))
    u=x+np.array(mix)@p['o'];h=norm(u,1)@p['w1']+p['b1'];g=np.array([[.5*a*(1+math.erf(a/2**.5)) for a in row] for row in h]);expected=u+g@p['w2']+p['b2'];before=x.copy()
    assert_allclose(m.vit_block(x,p),expected,atol=1e-10);assert_array_equal(x,before)
def permutation(m):
    p=params();p['q']=p['k']=p['v']=p['o']=np.eye(2);x=np.array([[1.,3.],[4.,2.],[0.,0.]])
    a=m.vit_block(x,p);b=m.vit_block(x[::-1],p);assert_allclose(a[::-1],b,atol=1e-10);assert np.isfinite(a).all()
def invalid(m):
    p=params();p['gamma']=np.ones((1,2))
    with np.testing.assert_raises(ValueError):m.vit_block(np.ones((1,2)),p)
    with np.testing.assert_raises(ValueError):m.vit_block(np.empty((0,2)),params())
    with np.testing.assert_raises(ValueError):m.vit_block(np.ones((1,2))*101,params())
TESTS=[('Residual identity','public',residual),('Final bias without postnorm','public',bias),('Scalar layernorm/attention/GELU oracle','hidden',oracle),('Permutation equivariance','hidden',permutation),('Validation','hidden',invalid)]

def scale_storage(m):
    rng=np.random.default_rng(222);x=rng.normal(size=(128,128))[:,::2];p=params(64,128);p['q']=p['k']=p['v']=p['o']=np.eye(64);saved=x.copy();out=m.vit_block(x,p);assert out.shape==(128,64) and out.dtype==np.float64 and np.isfinite(out).all();assert_allclose(m.vit_block(x[::-1],p),out[::-1],atol=1e-9);assert_allclose(x,saved)
    assert not np.shares_memory(out,x)
    for v in p.values():assert not np.shares_memory(out,v)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
