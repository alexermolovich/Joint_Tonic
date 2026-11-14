import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.teleop_quality_flags([0,1],[[0],[2]],[True,False],[-1],[1],[1]);assert_array_equal(r['missing'],[False,True]);assert_array_equal(r['out_of_range'],[False,True]);assert_array_equal(r['speed_jump'],[False,True])
def example2(m):
    r=m.teleop_quality_flags([0,.5],[[0],[1]],[True,True],[-1],[1],[2]);assert not any(v.any() for v in r.values())
def independent(m):
    r=m.teleop_quality_flags([0],[[2,-3]],[False],[-1,-2],[1,2],[1,1]);assert r['out_of_range'][0] and r['missing'][0] and not r['speed_jump'][0]
    q=np.array([[0.,0.],[0.,-1.],[0.,0.]]);copy=q.copy();r=m.teleop_quality_flags([0,.25,1],q,[True]*3,[-2]*2,[2]*2,[2]*2);assert_array_equal(r['speed_jump'],[False,True,False]);assert_array_equal(q,copy)
def invalid(m):
    good=[[0,1],[[0],[1]],[True,True],[-1],[1],[1]]
    for i,v in [(0,[0,0]),(1,[[np.nan],[1]]),(2,[1,1]),(3,[1]),(5,[0]),(1,[[0,1],[1,2]]),(0,[])]:
        args=good.copy();args[i]=v;bad(lambda:m.teleop_quality_flags(*args))
TESTS=[('Independent failure flags','public',example1),('Inclusive thresholds','public',example2),('Single and multichannel rows','hidden',independent),('Invalid quality inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    t=np.arange(4096,dtype=float);q=np.tile(t[:,None]*.1,(1,32))[:,::2];copy=q.copy();r=m.teleop_quality_flags(t,q,np.ones(4096,dtype=bool),np.full(16,-1.),np.full(16,1000.),np.full(16,.11))
    assert not any(v.any() for v in r.values());assert_array_equal(q,copy);assert all(v.dtype==bool and v.shape==(4096,) for v in r.values())

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
