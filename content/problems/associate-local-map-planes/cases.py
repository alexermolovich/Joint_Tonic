import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def corners():return np.array([[-1.,-1,0],[-1,1,0],[1,-1,0],[1,1,0]])
def first(m):
 r=m.associate_planes(np.array([[0.,0,1]]),corners(),4,2,0);assert r['valid'][0];assert_array_equal(r['neighbor_indices'],[[0,1,2,3]]);assert_allclose(r['normals'],[[0,0,1]]);assert_array_equal(r['offsets'],[0])
def line(m):
 r=m.associate_planes(np.zeros((1,3)),np.array([[0.,0,0],[1,0,0],[2,0,0]]),3,3,1);assert not r['valid'][0] and np.isnan(r['normals']).all()
def degeneracy(m):
 p=np.concatenate([np.eye(3),-np.eye(3)]);r=m.associate_planes(np.zeros((1,3)),p,6,1,1);assert not r['valid'][0]
 p=np.array([[1.,0,0],[-1,0,0],[0,1,0],[0,-1,0]]);r=m.associate_planes(np.zeros((1,3)),p,4,1,0);assert r['valid'][0]
 assert not m.associate_planes(np.zeros((1,3)),p,4,.99,0)['valid'][0]
 p=corners();p[-1,2]=.5;assert not m.associate_planes(np.zeros((1,3)),p,4,2,0)['valid'][0]
def scale(m):
 grid=np.array([[x*.1,y*.1,2.] for x in range(32) for y in range(32)],float);storage=np.zeros((len(grid),6));storage[:,::2]=grid;p=storage[:,::2];q=grid[::4]+[0,0,.1];before=p.copy();r=m.associate_planes(q,p,8,1,1e-12);assert r['valid'].all();assert_allclose(r['normals'],np.tile([0,0,1.],(256,1)),atol=1e-12);assert_allclose(r['offsets'],-2)
 for i in range(0,256,17):
  ids=sorted(range(len(p)),key=lambda j:(sum((float(p[j,d])-float(q[i,d]))**2 for d in range(3)),j))[:8];assert_array_equal(r['neighbor_indices'][i],ids)
 assert_array_equal(p,before);assert not np.shares_memory(r['centroids'],p)
 assert m.associate_planes(np.empty((0,3)),corners(),3,1,0)['neighbor_indices'].shape==(0,3)
def invalid(m):
 for k,r,t in [(2,1,0),(5,1,0),(True,1,0),(3,0,0),(3,1,-1),(3,1,10**1000)]:bad(lambda:m.associate_planes(np.zeros((1,3)),corners(),k,r,t))
 bad(lambda:m.associate_planes(np.zeros((1,2)),corners(),3,1,0))
TESTS=[('Planar neighbor fit and stable ties','public',first),('Collinear geometry','public',line),('Ambiguous normal and boundary gates','hidden',degeneracy),('Independent neighbors and full query scale','hidden',scale),('Invalid map contract','hidden',invalid)]
