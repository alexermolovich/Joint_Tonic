import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.normalize_observations({'p_cm':[[100],[200]]},{'position':'p_cm'},{'position':.01},[0,1]);assert_array_equal(r['features']['position'],[[1],[2]]);assert_array_equal(r['timestamps'],[0,1])
def example2(m):
    r=m.normalize_observations({'q':[[180]]},{'joint':'q','copy':'q'},{'joint':np.pi/180,'copy':1},[2]);assert_allclose(r['features']['joint'],[[np.pi]]);assert_array_equal(r['features']['copy'],[[180]])
def scale_storage(m):
    x=np.ones((4096,32))[:,::2];t=np.arange(4096.);r=m.normalize_observations({'x':x},{'a':'x','b':'x'},{'a':2,'b':3},t);assert np.all(r['features']['a']==2) and np.all(r['features']['b']==3);assert not np.shares_memory(r['features']['a'],x);assert not np.shares_memory(r['timestamps'],t)
def invalid(m):
    good=[{'x':[[1]]},{'a':'x'},{'a':1},[0]]
    for i,v in [(0,{'x':[[1]],'unused':[[np.nan]]}),(1,{'a':'missing'}),(2,{'a':0}),(2,{'a':1,'extra':2}),(0,{'bad-name':[[1]]}),(3,[0,1]),(2,{'a':True})]:
        a=good.copy();a[i]=v;bad(lambda:m.normalize_observations(*a))
TESTS=[('Canonical position units','public',example1),('Two explicit views of one field','public',example2),('Scale and independent storage','hidden',scale_storage),('Schema failures','hidden',invalid)]
