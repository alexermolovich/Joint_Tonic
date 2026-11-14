import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def column(m):
    r=m.contact_patch_statistics([[[False,True],[False,True]]]);assert_array_equal(r['area'],[2]);assert_allclose(r['centroid'],[[1,.5]]);assert_allclose(r['covariance'],[[[0,0],[0,.25]]]);assert_array_equal(r['bounds'],[[1,0,2,2]])
def single(m):
    x=np.zeros((2,3,4),bool);x[0,2,3]=True;r=m.contact_patch_statistics(x);assert_array_equal(r['centroid'][0],[3,2]);assert_array_equal(r['covariance'][0],np.zeros((2,2)));assert_array_equal(r['bounds'][0],[3,2,4,3]);assert np.isnan(r['centroid'][1]).all();assert_array_equal(r['bounds'][1],[-1]*4)
def scale(m):
    x=np.ones((128,64,128),bool)[:,:,::2];r=m.contact_patch_statistics(x);assert_array_equal(r['area'],np.full(128,4096));assert_allclose(r['centroid'],np.full((128,2),31.5));assert_allclose(r['covariance'],np.tile(np.eye(2)*(64**2-1)/12,(128,1,1)));assert not np.shares_memory(r['area'],x)
    x=np.array([[[True,False],[False,True]]]);r=m.contact_patch_statistics(x);assert_allclose(r['covariance'],np.full((1,2,2),.25))
def invalid(m):
    for x in [np.ones((1,2,2)),np.empty((1,0,2),bool),np.ones((1,2),bool)]:bad(lambda:m.contact_patch_statistics(x))
TESTS=[('Centroid and image covariance','public',column),('Single pixel and empty region','public',single),('Full image scale and cross covariance','hidden',scale),('Invalid masks','hidden',invalid)]
