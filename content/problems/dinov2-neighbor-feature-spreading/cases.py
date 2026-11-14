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
def args():return [f([[1,0],[-1,0]]),.01]
def example1(m):eq(checked(m.neighbor_spreading,args()),dict(loss=-math.log(2),distances=f([2,2]),neighbors=i([1,0])))
def example2(m):eq(m.neighbor_spreading(f([[1],[1],[1]]),.01),dict(loss=-math.log(.01),distances=f([0,0,0]),neighbors=i([1,0,0])))
def oracle(m):
 rng=np.random.default_rng(1008);x=rng.normal(size=(128,128))[:,::2];unit=[row/math.sqrt(sum(float(v)**2 for v in row)) for row in x];dist=[];nearest=[]
 for j,row in enumerate(unit):
  candidates=[(math.sqrt(sum(float(v)**2 for v in row-unit[k])),k) for k in range(128) if k!=j];d,k=min(candidates);dist.append(d);nearest.append(k)
 want=dict(loss=-sum(math.log(max(d,.001)) for d in dist)/128,distances=f(dist),neighbors=i(nearest));eq(checked(m.neighbor_spreading,[x,.001]),want);eq(m.neighbor_spreading(x*3,.001),want)
def invalid(m):
 a=args();generic_invalid(m.neighbor_spreading,a)
 for x,e in [(f([[0,0],[1,0]]),.01),(f([[1]]),.01),(f([[1e-10],[1]]),.01),(a[0],0),(a[0],True)]:rejected(lambda:m.neighbor_spreading(x,e))

def oversized_scalars(m):
    for value in (10**1000, -(10**1000)):
        values=args();values[-1]=value
        rejected(lambda: m.neighbor_spreading(*values))

TESTS=[('Oversized signed integer scalar','hidden',oversized_scalars),('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
