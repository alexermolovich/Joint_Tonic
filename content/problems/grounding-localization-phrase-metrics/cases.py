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
def args():return [f([[0,0,1,1]]),f([[0,0,1,1]]),i([1]),i([2]),b([True]),.5]
def expected(iou,box,phrase,grounded,count,lr,pr,gr):return dict(iou=f(iou),box_correct=b(box),phrase_correct=b(phrase),grounded_correct=b(grounded),count=count,localization_rate=lr,phrase_rate=pr,grounded_rate=gr)
def example1(m):eq(checked(m.grounding_pair_metrics,args()),expected([1],[1],[0],[0],1,1.,0.,0.))
def example2(m):
 a=args();a[0]=f([[0,0,.4,.4]]);a[1]=f([[.6,.6,1,1]]);a[3]=i([1]);eq(m.grounding_pair_metrics(*a),expected([0],[0],[1],[0],1,0.,1.,0.))
def oracle(m):
 a=[f([[0,0,1,1],[0,0,.5,1],[0,0,1,1]]),f([[0,0,.5,1],[.25,0,.75,1],[0,0,1,1]]),i([1,2,3]),i([1,2,3]),b([1,1,0]),.5];eq(checked(m.grounding_pair_metrics,a),expected([.5,1/3,0],[1,0,0],[1,1,0],[1,0,0],2,.5,1.,.5))
 a=[np.zeros((0,4)),np.zeros((0,4)),np.zeros(0,np.int64),np.zeros(0,np.int64),np.zeros(0,bool),0.];eq(m.grounding_pair_metrics(*a),expected([],[],[],[],0,0.,0.,0.))
 # Areas can underflow even though valid widths are positive; identical tiny boxes still have IoU1.
 a=args();a[0]=a[1]=f([[0,0,1e-200,1e-200]]);assert m.grounding_pair_metrics(*a)['iou'][0]==1
 a=[np.tile(f([[0,0,1,1]]),(4096,1)),np.tile(f([[0,0,1,1]]),(4096,1)),np.zeros(4096,np.int64),np.zeros(4096,np.int64),np.ones(4096,bool),1.];assert checked(m.grounding_pair_metrics,a)['grounded_rate']==1
def invalid(m):
 a=args();generic_invalid(m.grounding_pair_metrics,a)
 for index,value in [(0,f([[0,0,0,1]])),(1,f([[1,0,0,1]])),(2,i([-1])),(3,i([100001])),(5,True)]:
  q=a.copy();q[index]=value;rejected(lambda:m.grounding_pair_metrics(*q))

def oversized_scalars(m):
    for value in (10**1000, -(10**1000)):
        values=args();values[-1]=value
        rejected(lambda: m.grounding_pair_metrics(*values))

TESTS=[('Oversized signed integer scalar','hidden',oversized_scalars),('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
