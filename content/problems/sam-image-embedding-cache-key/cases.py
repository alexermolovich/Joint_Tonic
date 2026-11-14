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
def args():return ['0'*64,'1'*64,'2'*64,(4,8),None]
def expected(a):
 text='{"encoder_sha256":"'+a[1]+'","image_sha256":"'+a[0]+'","preprocessing_sha256":"'+a[2]+'","resized_shape":['+str(a[3][0])+','+str(a[3][1])+'],"schema":1}'
 return hashlib.sha256(text.encode('ascii')).hexdigest()
def example1(m):
 a=args();key=expected(a);eq(m.embedding_cache_key(*a),dict(key=key,hit=False));a[-1]=key;eq(m.embedding_cache_key(*a),dict(key=key,hit=True))
def example2(m):
 a=args();a[-1]=expected(a);a[2]='3'*64;eq(m.embedding_cache_key(*a),dict(key=expected(a),hit=False))
def oracle(m):
 a=args();old=expected(a)
 for index,value in [(0,'f'*64),(1,'e'*64),(2,'d'*64),(3,(8,4)),(3,(8192,1))]:
  q=a.copy();q[index]=value;q[-1]=old;eq(checked(m.embedding_cache_key,q),dict(key=expected(q),hit=False));assert expected(q)!=old
def invalid(m):
 a=args()
 for index,value in [(0,'A'*64),(1,'a'*63),(2,bytes(64)),(3,[4,8]),(3,(True,8)),(3,(0,8)),(3,(4,8,1)),(4,'x'*64)]:
  q=a.copy();q[index]=value;rejected(lambda:m.embedding_cache_key(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
