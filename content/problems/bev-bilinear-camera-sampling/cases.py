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
def args():return [f([[[[0],[2]],[[4],[6]]]]),f([[[.5,.5]]]),b([[True]])]
def example1(m):eq(checked(m.sample_camera_features,args()),dict(samples=f([[[3]]]),used=b([[True]])))
def example2(m):
 a=args();a[1]=f([[[1,1],[1.1,1]]]);a[2]=b([[True,True]]);eq(m.sample_camera_features(*a),dict(samples=f([[[6],[0]]]),used=b([[True,False]])))
def oracle(m):
 rng=np.random.default_rng(1005);features=rng.normal(size=(3,4,10,2))[:,:,::2];coord=rng.uniform(-1,5,size=(3,40,2));valid=rng.random((3,40))>.2
 want=np.zeros((3,40,2));used=np.zeros((3,40),bool)
 for c in range(3):
  for n,(u,v) in enumerate(coord[c]):
   if valid[c,n] and 0<=u<=4 and 0<=v<=3:
    used[c,n]=True
    for y in range(4):
     for x in range(5):want[c,n]+=max(0,1-abs(u-x))*max(0,1-abs(v-y))*features[c,y,x]
 eq(checked(m.sample_camera_features,[features,coord,valid]),dict(samples=want,used=used))
 eq(m.sample_camera_features(np.ones((1,1,1,1)),np.zeros((1,0,2)),np.ones((1,0),bool)),dict(samples=np.zeros((1,0,1)),used=np.ones((1,0),bool)))
 # Regression for advertised maximum (1,048,576 entries), above the former common cap.
 out=checked(m.sample_camera_features,[np.ones((8,64,64,32)),np.zeros((8,4096,2)),np.ones((8,4096),bool)]);eq(out['samples'],np.ones((8,4096,32)))
def invalid(m):
 a=args();generic_invalid(m.sample_camera_features,a)
 for index,value in [(0,np.zeros((0,1,1,1))),(1,np.zeros((2,1,2))),(2,b([[True,False]]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.sample_camera_features(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
