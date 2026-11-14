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
def args():return [np.full((1,1,1,1,1),.5),f([[[2]]]),b([[1]]),b([[1]]),f([[3]]),f([[4]]),f([1])]
def example1(m):eq(checked(m.encode_observation_window,args()),dict(tokens=f([[[10.5]]]),flat=f([[10.5]]),used=b([[1]])))
def example2(m):
 a=args();a[3][:]=False;eq(m.encode_observation_window(*a),dict(tokens=f([[[0]]]),flat=f([[0]]),used=b([[0]])))
def oracle(m):
 rng=np.random.default_rng(1011);a=[rng.uniform(size=(2,3,3,4,8))[...,::2],rng.normal(size=(2,3,2)),rng.random((2,3))>.2,rng.random((2,3))>.3,rng.normal(size=(3,4)),rng.normal(size=(2,4)),rng.normal(size=4)];want=np.zeros((2,3,4));used=a[2]&a[3]
 for bb in range(2):
  for t in range(3):
   if used[bb,t]:
    for d in range(4):want[bb,t,d]=sum(sum(float(v) for v in a[0][bb,t,c].flat)/16*a[4][c,d] for c in range(3))+sum(a[1][bb,t,p]*a[5][p,d] for p in range(2))+a[6][d]
 eq(checked(m.encode_observation_window,a),dict(tokens=want,flat=want.reshape(2,12).copy(),used=used))
 a=[np.ones((8,8,3,32,32)),np.ones((8,8,32)),np.ones((8,8),bool),np.ones((8,8),bool),np.ones((3,32)),np.ones((32,32)),np.ones(32)];eq(checked(m.encode_observation_window,a)['tokens'],np.full((8,8,32),36.))
def invalid(m):
 a=args();generic_invalid(m.encode_observation_window,a)
 for index,value in [(0,np.full((1,1,1,1,1),1.1)),(1,np.zeros((1,2,1))),(4,f([[3,4]])),(2,b([1]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.encode_observation_window(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
