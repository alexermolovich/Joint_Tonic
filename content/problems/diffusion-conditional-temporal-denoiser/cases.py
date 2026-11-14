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
def args():return [f([[[0]]]),f([0]),f([[0]]),np.zeros((3,1,1)),np.zeros((1,2)),np.zeros((2,2)),f([[1]]),f([2])]
def example1(m):eq(checked(m.conditional_denoiser,args()),f([[[2]]]))
def example2(m):
 a=args();a[0][:]=1;a[3][1]=1;a[-1][:]=0;eq(m.conditional_denoiser(*a),f([[[1/(1+math.exp(-1))]]]))
def oracle(m):
 rng=np.random.default_rng(1012);a=[rng.normal(size=(2,4,2)),f([.25,.75]),rng.normal(size=(2,3)),rng.normal(size=(3,2,2)),rng.normal(size=(3,4)),rng.normal(size=(2,4)),rng.normal(size=(2,2)),rng.normal(size=2)];want=np.zeros((2,4,2))
 for bb in range(2):
  film=[sum(a[2][bb,f0]*a[4][f0,c] for f0 in range(3))+math.sin(math.pi*a[1][bb])*a[5][0,c]+math.cos(math.pi*a[1][bb])*a[5][1,c] for c in range(4)]
  for t in range(4):
   hidden=[]
   for c in range(2):
    conv=sum(a[0][bb,t+k-1,j]*a[3][k,j,c] for k in range(3) if 0<=t+k-1<4 for j in range(2));z=(1+film[c])*conv+film[c+2];hidden.append(z/(1+math.exp(-z)))
   for j in range(2):want[bb,t,j]=sum(hidden[c]*a[6][c,j] for c in range(2))+a[7][j]
 eq(checked(m.conditional_denoiser,a),want)
 a=[np.full((8,32,8),100.),np.ones(8),np.full((8,16),100.),np.full((3,8,16),-100.),np.full((16,32),100.),np.full((2,32),100.),np.ones((16,8)),np.zeros(8)];out=checked(m.conditional_denoiser,a);assert np.isfinite(out).all();assert_allclose(out,0,atol=0)
def invalid(m):
 a=args();generic_invalid(m.conditional_denoiser,a)
 for index,value in [(0,f([[[101]]])),(1,f([1.1])),(3,np.zeros((2,1,1))),(4,np.zeros((1,3))),(6,np.ones((2,1)))]:
  q=a.copy();q[index]=value;rejected(lambda:m.conditional_denoiser(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
