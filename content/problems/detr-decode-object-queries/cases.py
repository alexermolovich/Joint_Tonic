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
def args():return [f([[[0,0]]]),f([[[.5,.5,1,1]]]),b([[False]]),.5]
def example1(m):eq(checked(m.decode_queries,args()),dict(boxes=f([[[0,0,1,1]]]),scores=f([[.5]]),labels=i([[0]]),valid=b([[True]])))
def example2(m):
 a=args();a[-1]=.6;eq(m.decode_queries(*a),dict(boxes=f([[[0,0,0,0]]]),scores=f([[0]]),labels=i([[-1]]),valid=b([[False]])))
def oracle(m):
 a=[f([[[1000,1000,1000],[2,-3,8],[-1000,-1000,-1000]]]),f([[[0,1,1,1],[.5,.5,.4,.6],[1,0,1,1]]]),b([[False,False,True]]),0.]
 out=checked(m.decode_queries,a);eq(out['labels'],i([[0,0,-1]]));eq(out['scores'],f([[1/3,math.exp(2)/(math.exp(2)+math.exp(-3)+math.exp(8)),0]]));eq(out['boxes'],f([[[0,.5,.5,1],[.3,.2,.7,.8],[0,0,0,0]]]))
 # Full stated query dimensions, including padding, and a noncontiguous feature view.
 a=[np.ones((16,128,130))[:,:,::2],np.ones((16,128,4)),np.zeros((16,128),bool),1/65]
 out=checked(m.decode_queries,a);assert out['valid'].all();eq(out['scores'],np.full((16,128),1/65))
def invalid(m):
 a=args();generic_invalid(m.decode_queries,a)
 for index,value in [(0,np.zeros((1,1,1))),(1,f([[[-.1,0,0,0]]])),(2,b([False])),(3,True),(3,-.1)]:
  q=a.copy();q[index]=value;rejected(lambda:m.decode_queries(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
