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
def args():return [f([[[1,3]]]),f([1,1]),f([0,0]),np.eye(2),f([0,0]),1.]
def example1(m):eq(checked(m.class_token_logits,args()),f([[-1/math.sqrt(2),1/math.sqrt(2)]]))
def example2(m):eq(m.class_token_logits(f([[[99]]]),f([2]),f([3]),f([[4]]),f([5]),1e-8),f([[17]]))
def oracle(m):
 rng=np.random.default_rng(1002);a=[rng.normal(size=(4,5,6))[:,:,::2],rng.normal(size=3),rng.normal(size=3),rng.normal(size=(3,2)),rng.normal(size=2),.01]
 want=[]
 for row in a[0][:,0]:
  mean=sum(row)/3;var=sum((float(v)-mean)**2 for v in row)/3
  norm=[(float(row[j])-mean)/math.sqrt(var+.01)*a[1][j]+a[2][j] for j in range(3)]
  want.append([sum(norm[j]*a[3][j,k] for j in range(3))+a[4][k] for k in range(2)])
 eq(checked(m.class_token_logits,a),f(want));a[0][:,1:]=999;eq(m.class_token_logits(*a),f(want))
 a=[np.ones((32,257,64)),np.ones(64),np.zeros(64),np.eye(64),np.zeros(64),1e-8];eq(checked(m.class_token_logits,a),np.zeros((32,64)))
def invalid(m):
 a=args();generic_invalid(m.class_token_logits,a)
 for index,value in [(0,np.zeros((1,0,2))),(1,f([1])),(3,np.ones((3,2))),(5,False),(5,0.)]:
  q=a.copy();q[index]=value;rejected(lambda:m.class_token_logits(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
