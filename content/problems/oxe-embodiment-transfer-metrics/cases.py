import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.embodiment_transfer_metrics([0,0,0],[0,1,1],[True,True,False],2);assert_array_equal(r['count'],[[1,2],[0,0]]);assert_allclose(r['success_rate'],[[1,.5],[np.nan,np.nan]],equal_nan=True);assert r['same_embodiment_rate']==1 and r['transfer_rate']==.5
def example2(m):
    r=m.embodiment_transfer_metrics([1],[1],[False],2);assert r['same_embodiment_rate']==0 and r['transfer_rate'] is None;assert r['count'][1,1]==1
def micro_scale(m):
    t=np.zeros(10000,dtype=int);e=np.r_[np.ones(9000,dtype=int),np.full(1000,2,dtype=int)];y=np.r_[np.ones(9000,dtype=bool),np.zeros(1000,dtype=bool)];r=m.embodiment_transfer_metrics(t,e,y,3);assert r['transfer_rate']==.9 and r['same_embodiment_rate'] is None
    r=m.embodiment_transfer_metrics(np.array([],dtype=int),np.array([],dtype=int),np.array([],dtype=bool),1);assert r['transfer_rate'] is None and np.isnan(r['success_rate']).all()
def invalid(m):
    for a in [([0],[1],[True],1),([0.],[0],[True],1),([0],[0],[1],1),([-1],[0],[True],1),([0],[0],[True],0),([0],[0,0],[True],1)]:bad(lambda:m.embodiment_transfer_metrics(*a))
TESTS=[('Directional transfer matrix','public',example1),('No transfer evidence','public',example2),('Micro weighting and empty evidence','hidden',micro_scale),('Invalid episode labels','hidden',invalid)]
