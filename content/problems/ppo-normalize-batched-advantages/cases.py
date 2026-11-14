import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def two(m):
    r=m.normalize_advantages([[1,3]],[[True,True]],1);assert r['mean']==2 and r['count']==2;assert_allclose(r['std'],np.sqrt(2));assert_allclose(r['normalized'],[[-1/np.sqrt(2),1/np.sqrt(2)]])
def masked(m):
    r=m.normalize_advantages([[4,99]],[[True,False]],1);assert r['mean']==4 and r['std']==1 and r['count']==1;assert_array_equal(r['normalized'],[[0,0]])
def scale(m):
    a=np.arange(64*2048.).reshape(64,2048)[:,::2];mask=np.ones_like(a,dtype=bool);mask[:,::3]=False;r=m.normalize_advantages(a,mask,1e-6);assert_allclose(r['mean'],a[mask].mean());assert_allclose(r['normalized'][mask].mean(),0,atol=1e-12);assert not r['normalized'][~mask].any();assert not np.shares_memory(r['normalized'],a)
    r=m.normalize_advantages([[9]],[[False]],.25);assert r['count']==0 and r['std']==.5 and r['mean']==0

def invalid(m):
    for args in [([[1]],[[1]],1),([[1]],[[True]],0),([[1]],[[True]],True),([[np.nan]],[[False]],1)]:bad(lambda:m.normalize_advantages(*args))
TESTS=[('Population variance','public',two),('Real value versus padding','public',masked),('Scale and empty support','hidden',scale),('Invalid statistics','hidden',invalid)]
