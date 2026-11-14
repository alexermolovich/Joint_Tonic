import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    p,a=m.resample_particles([1,0,2,1],.5); assert_allclose(p,[.25,0,.5,.25]); assert_array_equal(a,[0,2,2,3])
def boundary(m):
    p,a=m.resample_particles([0,5],0); assert_allclose(p,[0,1]); assert_array_equal(a,[1,1])
def tiny(m):
    p,a=m.resample_particles([1e-300,1e-300],.5); assert_allclose(p,[.5,.5]); assert_array_equal(a,[0,1])
    p,a=m.resample_particles([3],.99); assert p.dtype==np.float64 and a.dtype==np.int64; assert_array_equal(a,[0])
def oracle(m):
    w=np.array([1.,2,0,4,3]); old=w.copy(); p,a=m.resample_particles(w,.25); cumulative=np.cumsum(w/w.sum())
    expected=[next(i for i,c in enumerate(cumulative) if c>(.25+k)/len(w)) for k in range(len(w))]
    assert_array_equal(a,expected); assert_array_equal(w,old); assert_allclose(p.sum(),1)
    assert_array_equal(m.resample_particles(w*100,.25)[1],a)
def invalid(m):
    for args in [([],0),([0,0],0),([-1,2],0),([[1]],0),([1],1),([1],-1),([True],0),([np.nan],0),([1],[0])]:
        with np.testing.assert_raises(ValueError): m.resample_particles(*args)
TESTS=[('Systematic positions','public',example),('Zero-mass boundary','public',boundary),('Tiny mass and one particle','hidden',tiny),('Cumulative interval oracle','hidden',oracle),('Invalid particle contract','hidden',invalid)]

def near_one_offset(m):
    p,a=m.resample_particles([1,1,1],np.nextafter(1.,0.))
    assert a.min()>=0 and a.max()<3
    assert_array_equal(a,[1,2,2])
TESTS.append(('Largest representable subunit offset','hidden',near_one_offset))
