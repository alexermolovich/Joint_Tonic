import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    r=m.audit_cloud(np.array([[0.,0,0],[50,0,0],[100,0,0]]),'cm','base','base',1.)
    assert r['frame_matches'] is True and r['occupied_voxels']==2 and r['points_per_voxel']==1.5;assert_allclose(r['extent_m'],[1,0,0])
def negative(m):
    r=m.audit_cloud(np.array([[-.01,0,0],[0,0,0]]),'m','camera','base',1.);assert r['occupied_voxels']==2 and r['frame_matches'] is False
def invariants(m):
    p=np.array([[0.,0,0],[1,2,3],[1,2,3],[2,4,6]])
    a=m.audit_cloud(p,'m','a','a',.5);b=m.audit_cloud(p*1000,'mm','a','a',.5);assert a['occupied_voxels']==b['occupied_voxels']==3;assert_allclose(a['extent_m'],b['extent_m']);assert a['points_per_voxel']==4/3
    z=m.audit_cloud(np.empty((0,3)),'m','a','a',1);assert z['occupied_voxels']==0 and z['points_per_voxel']==0;assert_array_equal(z['extent_m'],[0,0,0])
def oracle(m):
    import math
    p=np.random.default_rng(19).uniform(-2,2,(4096,3));copy=p.copy();r=m.audit_cloud(p,'m','a','b',.25);expected={tuple(math.floor(float(v)/.25) for v in row) for row in p};assert r['occupied_voxels']==len(expected);assert_allclose(r['points_per_voxel'],len(p)/len(expected));assert_array_equal(p,copy)
def invalid(m):
    for p,u,f,e,h in [(np.zeros((1,2)),'m','a','a',1),(np.zeros((1,3)),'inch','a','a',1),(np.zeros((1,3)),'m','','a',1),(np.zeros((1,3)),'m','a','a',True),(np.zeros((1,3)),'m','a','a',np.nan),(np.zeros((1,3)),'m','a','a',0)]:
        with np.testing.assert_raises(ValueError):m.audit_cloud(p,u,f,e,h)
TESTS=[('Unit conversion','public',example),('Negative voxel and frame mismatch','public',negative),('Unit invariance duplicates and empty','hidden',invariants),('Independent voxel set','hidden',oracle),('Validation','hidden',invalid)]
