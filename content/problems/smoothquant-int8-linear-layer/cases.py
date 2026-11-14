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
 qx,qw,sx,sw,y=m.quantize_int8_layer(arr([[127,0]]),arr([[1],[0]]));equal(qx,[[127,0]],np.int8);equal(qw,[[127],[0]],np.int8);equal(sx,[[1]]);equal(sw,[[1/127]]);equal(y,[[127]])
def example2(m):
 a,b,c,d,e=m.quantize_int8_layer(arr([[0,0]]),arr([[0],[0]]));equal(a,[[0,0]],np.int8);equal(b,[[0],[0]],np.int8);equal(c,[[1]]);equal(d,[[1]]);equal(e,[[0]])
def edges(m):
 a,b,c,d,e=m.quantize_int8_layer(arr([[.5,1.5,2.5,127]]),arr([[127],[0],[0],[0]]));equal(a,[[0,2,2,127]],np.int8);equal(e,[[0]])
 a,b,c,d,e=m.quantize_int8_layer(np.full((1,32),127,dtype=np.float32),np.full((32,1),127,dtype=np.float32));equal(e,[[32*127*127]])
 a,b,c,d,e=m.quantize_int8_layer(np.array([[1e-38]],dtype=np.float32),np.array([[2e-38]],dtype=np.float32));assert a[0,0]==127 and b[0,0]==127;assert e[0,0]>0

def oracle(m):
 rng=np.random.default_rng(22);x=rng.normal(size=(32,128))[:,::2];w=rng.normal(size=(64,32))[:,::2];before=[x.copy(),w.copy()]
 a,b,sx,sw,y=m.quantize_int8_layer(x,w);xs=[max(abs(float(v)) for v in row)/127 or 1 for row in x];ws=[max(abs(float(v)) for v in w[:,j])/127 or 1 for j in range(16)]
 qa=[[max(-127,min(127,round(float(x[i,j])/xs[i]))) for j in range(64)] for i in range(32)];qb=[[max(-127,min(127,round(float(w[j,k])/ws[k]))) for k in range(16)] for j in range(64)]
 out=[[sum(qa[i][j]*qb[j][k] for j in range(64))*xs[i]*ws[k] for k in range(16)] for i in range(32)]
 equal(a,qa,np.int8);equal(b,qb,np.int8);equal(y,out);equal(sx,np.array(xs)[:,None]);equal(sw,[ws]);preserve(before,[x,w])
def invalid(m):
 for x,w in [(np.zeros((0,1)),arr([[1]])),(np.ones((1024,1024)),np.ones((1024,16))),(arr([[1]]),np.array([[True]])),(arr([[np.inf]]),arr([[1]]))]:reject(lambda:m.quantize_int8_layer(x,w))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
