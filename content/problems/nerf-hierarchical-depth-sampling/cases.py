import numpy as np
import math, hashlib, json, copy
from numpy.testing import assert_allclose, assert_array_equal
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)
def eq(got,want):
    if isinstance(want,dict):
        assert isinstance(got,dict) and got.keys()==want.keys()
        for k in want:eq(got[k],want[k])
    elif isinstance(want,np.ndarray):
        assert isinstance(got,np.ndarray) and got.shape==want.shape and got.dtype==want.dtype
        assert_allclose(got,want,rtol=1e-6,atol=1e-7)
    else:
        assert type(got) is type(want)
        if isinstance(want,float):assert_allclose(got,want,rtol=1e-6,atol=1e-7)
        else:assert got==want
def rejected(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def checked(fn,args):
    before=copy.deepcopy(args);out=fn(*args)
    arrays=[v for v in args if isinstance(v,np.ndarray)]
    for old,new in zip(before,args):
        if isinstance(old,np.ndarray):assert_array_equal(old,new)
        else:assert old==new
    values=list(out.values()) if isinstance(out,dict) else [out]
    for x in values:
        if isinstance(x,np.ndarray):
            for a in arrays:assert not np.shares_memory(x,a)
            for y in values:
                if isinstance(y,np.ndarray) and y is not x:assert not np.shares_memory(x,y)
    return out
def generic_invalid(fn,args):
    for index,a in enumerate(args):
        if isinstance(a,np.ndarray):
            bad=list(args);bad[index]=a.tolist();rejected(lambda:fn(*bad))
            bad=list(args);bad[index]=a.astype(np.float32) if a.dtype==np.float64 else a.astype(np.float64);rejected(lambda:fn(*bad))
            if a.dtype==np.float64 and a.size:
                for value in (np.nan,np.inf,1000001.):
                    bad=list(args);bad[index]=a.copy();bad[index].flat[0]=value;rejected(lambda:fn(*bad))
def args():return [f([[0,1,3]]),f([[0,0]]),f([[0,.25,.5,.75,1]])]
def example1(m):eq(checked(m.hierarchical_samples,args()),f([[0,.5,1,2,3]]))
def example2(m):eq(m.hierarchical_samples(f([[2,6]]),f([[5]]),f([[.75,.25]])),f([[5,3]]))
def oracle(m):
 rng=np.random.default_rng(1006);edges=np.tile(np.linspace(0,1000,129),(32,1));weights=rng.uniform(0,100,size=(32,128));q=rng.uniform(size=(32,128));out=checked(m.hierarchical_samples,[edges,weights,q])
 # Verify the defining inverse-CDF property with an independently reconstructed forward CDF.
 for row in range(32):
  masses=[float(v)+1e-5 for v in weights[row]];total=sum(masses)
  for k,x in enumerate(out[row]):
   j=min(int(x/(1000/128)),127);cdf=(sum(masses[:j])+masses[j]*(x-edges[row,j])/(edges[row,j+1]-edges[row,j]))/total
   assert_allclose(cdf,q[row,k],rtol=1e-6,atol=1e-7)
 out=m.hierarchical_samples(f([[0,1,10]]),f([[1e6,0]]),f([[0,1,.5]]));assert_allclose(out,[[0,10,.5]],atol=1e-7)
def invalid(m):
 a=args();generic_invalid(m.hierarchical_samples,a)
 for index,value in [(0,f([[0,1,1]])),(1,f([[0,-1]])),(2,f([[1.1]])),(0,f([[0,1e-10,1]]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.hierarchical_samples(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
