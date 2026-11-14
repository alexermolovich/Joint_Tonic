"""Original deterministic synthetic fixtures; CC0-1.0."""
import numpy as np
import math

def arr(x):return np.array(x,dtype=np.float64)
def equal(actual,expected,dtype=np.float64):
    assert isinstance(actual,np.ndarray) and actual.dtype==np.dtype(dtype)
    assert actual.shape==np.asarray(expected).shape
    np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-10)
def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def preserve(before,after):
    for a,b in zip(before,after):np.testing.assert_array_equal(a,b)

def example1(m):
 s,z,q,w=m.groupwise_quantize_weights(arr([[-1,1,0,3]]),2,2);equal(s,[[2/3,1]]);equal(z,[[2,0]],np.int64);equal(q,[[0,3,0,3]],np.uint8);equal(w,[[-4/3,2/3,0,3]])
def example2(m):
 s,z,q,w=m.groupwise_quantize_weights(arr([[0,0]]),2,4);equal(s,[[1]]);equal(z,[[0]],np.int64);equal(q,[[0,0]],np.uint8);equal(w,[[0,0]])
def edges(m):
 s,z,q,w=m.groupwise_quantize_weights(arr([[-1,.5,2]]),3,2);equal(q,[[0,1,3]],np.uint8);equal(w,[[-1,0,2]])
 s,z,q,w=m.groupwise_quantize_weights(np.array([[1e-38,2e-38]],dtype=np.float32),2,8);assert w.dtype==np.float64 and s[0,0]>0;assert q[0,1]==255
 s,z,q,w=m.groupwise_quantize_weights(arr([[2,2,-3,-3]]),2,2);equal(q,[[3,3,0,0]],np.uint8);equal(w,[[2,2,-3,-3]])
 s,z,q,w=m.groupwise_quantize_weights(arr([[np.nextafter(0.,1.)]]),1,8);assert s[0,0]==np.finfo(np.float64).tiny;assert np.isfinite(w).all() and q[0,0]==0

def oracle(m):
 rng=np.random.default_rng(29);a=rng.uniform(-3,5,size=(64,256))[:,::2];before=a.copy();s,z,q,w=m.groupwise_quantize_weights(a,8,4)
 es=[];ez=[];eq=[];ew=[]
 for row in a:
  rs=[];rz=[];rq=[];rw=[]
  for start in range(0,128,8):
   chunk=[float(v) for v in row[start:start+8]];lo=min(0,*chunk);hi=max(0,*chunk);scale=(hi-lo)/15 or 1;zero=max(0,min(15,round(-lo/scale)));codes=[max(0,min(15,round(v/scale)+zero)) for v in chunk]
   rs.append(scale);rz.append(zero);rq.extend(codes);rw.extend((v-zero)*scale for v in codes)
  es.append(rs);ez.append(rz);eq.append(rq);ew.append(rw)
 equal(s,es);equal(z,ez,np.int64);equal(q,eq,np.uint8);equal(w,ew);np.testing.assert_array_equal(a,before);assert not np.shares_memory(w,a)
def invalid(m):
 for a,g,b in [(arr([[1,2,3]]),2,4),(arr([[1]]),True,4),(arr([[1]]),1,1),(arr([[1]]),1,9),(arr([[np.nan]]),1,4),(np.array([[1]]),1,4),(np.empty((0,1)),1,4)]:reject(lambda:m.groupwise_quantize_weights(a,g,b))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
