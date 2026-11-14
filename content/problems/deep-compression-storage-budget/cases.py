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

def call(m,n,f,l,i,c,h):return m.compressed_storage_budget(n,np.array(f,dtype=np.int64),np.array(l,dtype=np.int64),i,c,h)
def example1(m):
 r=call(m,10,[3,2],[1,1],3,32,2);assert r=={'symbol_bits':5,'symbol_bytes':1,'index_bytes':2,'codebook_bytes':8,'total_bytes':13,'dense_bytes':40,'compression_ratio':40/13}
def example2(m):
 r=call(m,1,[0],[1],1,16,0);assert r=={'symbol_bits':0,'symbol_bytes':0,'index_bytes':0,'codebook_bytes':2,'total_bytes':2,'dense_bytes':4,'compression_ratio':2.}
def edges(m):
 r=call(m,10**12,[10**12],[32],64,16,10**6);assert r['symbol_bits']==32*10**12 and r['index_bytes']==8*10**12 and r['total_bytes']==12*10**12+1000002
 assert all(type(r[k]) is int for k in r if k!='compression_ratio')
 r=call(m,2,[1,1],[1,1],1,16,0);assert r['symbol_bytes']==1 and r['index_bytes']==1 and r['total_bytes']==6

def oracle(m):
 rng=np.random.default_rng(27);f=rng.integers(0,10000,size=512,dtype=np.int64)[::2];lengths=np.full(256,8,dtype=np.int64);before=[f.copy(),lengths.copy()];n=sum(int(v) for v in f);r=m.compressed_storage_budget(n+123,f,lengths,17,32,99)
 expected=sum(int(v)*8 for v in f);indices=math.ceil(n*17/8);total=math.ceil(expected/8)+indices+256*4+99
 assert r['symbol_bits']==expected and r['total_bytes']==total and r['dense_bytes']==4*(n+123);assert r['compression_ratio']==4*(n+123)/total;preserve(before,[f,lengths])
def invalid(m):
 for args in [(3,[1,1,1],[1,1,1],2,32,0),(1,[2],[1],2,32,0),(1,[-1],[1],2,32,0),(1,[1],[0],2,32,0),(1,[1],[33],2,32,0),(1,[1],[1],0,32,0),(1,[1],[1],2,8,0),(True,[1],[1],2,32,0)]:reject(lambda:call(m,*args))
 reject(lambda:m.compressed_storage_budget(1,np.array([1],dtype=np.int32),np.array([1],dtype=np.int64),1,32,0))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
