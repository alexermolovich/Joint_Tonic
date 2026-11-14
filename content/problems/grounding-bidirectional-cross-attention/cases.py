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
def args():return [f([[[1]]]),f([[[0],[0]]]),b([[True]]),b([[True,True]])]
def example1(m):eq(checked(m.bidirectional_context,args()),dict(image_context=f([[[0]]]),text_context=f([[[1],[1]]]),image_weights=f([[[.5,.5]]]),text_weights=f([[[1],[1]]])))
def example2(m):
 a=args();a[-1][:]=False;eq(m.bidirectional_context(*a),dict(image_context=np.zeros((1,1,1)),text_context=np.zeros((1,2,1)),image_weights=np.zeros((1,1,2)),text_weights=np.zeros((1,2,1))))
def oracle(m):
 rng=np.random.default_rng(1009);im=rng.normal(size=(2,4,6))[:,:,::2];tx=rng.normal(size=(2,5,3));iv=b([[1,1,0,1],[0,0,0,0]]);tv=b([[1,0,1,0,1],[1,1,1,1,1]]);out=checked(m.bidirectional_context,[im,tx,iv,tv])
 for query,key,qmask,kmask,weight,context in [(im,tx,iv,tv,out['image_weights'],out['image_context']),(tx,im,tv,iv,out['text_weights'],out['text_context'])]:
  for batch in range(2):
   for j in range(query.shape[1]):
    row=np.zeros(key.shape[1]);ks=np.flatnonzero(kmask[batch])
    if qmask[batch,j] and len(ks):
     scores=[sum(query[batch,j,d]*key[batch,k,d] for d in range(3))/math.sqrt(3) for k in ks];ex=[math.exp(v-max(scores)) for v in scores]
     for k,e in zip(ks,ex):row[k]=e/sum(ex)
    eq(weight[batch,j],row);eq(context[batch,j],sum((row[k]*key[batch,k] for k in range(key.shape[1])),np.zeros(3)))
 a=[np.full((8,128,64),1e6),np.full((8,64,64),-1e6),np.ones((8,128),bool),np.ones((8,64),bool)];out=checked(m.bidirectional_context,a);eq(out['image_weights'],np.full((8,128,64),1/64))
def invalid(m):
 a=args();generic_invalid(m.bidirectional_context,a)
 for index,value in [(0,np.zeros((1,0,1))),(1,np.zeros((1,2,2))),(2,b([True]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.bidirectional_context(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
