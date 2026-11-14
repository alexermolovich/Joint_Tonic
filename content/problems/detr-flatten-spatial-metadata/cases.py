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
def args():return [f([[[[2],[4]]]]),f([[[10],[20]]]),b([[[True,False]]])]
def example1(m):eq(checked(m.flatten_spatial,args()),dict(tokens=f([[[2],[0]]]),position_tokens=f([[[10],[0]]]),padding=b([[False,True]]),coordinates=i([[0,0],[0,1]])))
def example2(m):
 a=args();a[2][:]=False;eq(m.flatten_spatial(*a),dict(tokens=np.zeros((1,2,1)),position_tokens=np.zeros((1,2,1)),padding=np.ones((1,2),bool),coordinates=i([[0,0],[0,1]])))
def oracle(m):
 rng=np.random.default_rng(1001);a=[rng.normal(size=(2,3,8,4))[:,:,::2],rng.normal(size=(3,4,4)),rng.random((2,3,4))>.4];out=checked(m.flatten_spatial,a)
 for batch in range(2):
  for row in range(3):
   for col in range(4):
    index=row*4+col;on=a[2][batch,row,col];eq(out['tokens'][batch,index],a[0][batch,row,col] if on else np.zeros(4));eq(out['position_tokens'][batch,index],a[1][row,col] if on else np.zeros(4));eq(out['coordinates'][index],i([row,col]))
 a=[np.zeros((16,32,32,32)),np.ones((32,32,32)),np.ones((16,32,32),bool)];assert checked(m.flatten_spatial,a)['tokens'].shape==(16,1024,32)
def invalid(m):
 a=args();generic_invalid(m.flatten_spatial,a)
 for index,value in [(0,np.zeros((1,0,1,1))),(1,np.zeros((2,1,1))),(2,b([[True,False]]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.flatten_spatial(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
