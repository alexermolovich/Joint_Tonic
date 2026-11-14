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
def args():return [f([[0,0],[4,2]]),2,4,8]
def example1(m):eq(checked(m.resize_prompt_coordinates,args()),dict(points=f([[0,0],[8,4]]),resized_shape=i([4,8])))
def example2(m):eq(m.resize_prompt_coordinates(f([[2.5,1.5]]),3,5,4),dict(points=f([[2,1]]),resized_shape=i([2,4])))
def oracle(m):
 eq(m.resize_prompt_coordinates(np.zeros((0,2)),3,5,4),dict(points=np.zeros((0,2)),resized_shape=i([2,4])))
 points=np.tile(f([[2.5,1.5,99,99]]),(4096,1))[:,:2]
 assert not points.flags.c_contiguous
 eq(checked(m.resize_prompt_coordinates,[points,3,5,4]),dict(points=np.tile(f([[2,1]]),(4096,1)),resized_shape=i([2,4])))
 for h,w,l in [(7,4,9),(8192,8192,2048),(3,6,1)]:
  points=f([[w,h],[w/3,h/7]])[:,::-1][:,::-1];hh=int(h*l/max(h,w)+.5);ww=int(w*l/max(h,w)+.5)
  eq(checked(m.resize_prompt_coordinates,[points,h,w,l]),dict(points=f([[ww,hh],[ww/3,hh/7]]),resized_shape=i([hh,ww])))
def invalid(m):
 a=args();generic_invalid(m.resize_prompt_coordinates,a)
 for values in [[f([[4.1,0]]),2,4,8],[np.zeros((1,3)),2,4,8],[f([[0,0]]),1,8192,1],[f([[0,0]]),True,4,8],[f([[0,0]]),2,4,0]]:rejected(lambda:m.resize_prompt_coordinates(*values))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
