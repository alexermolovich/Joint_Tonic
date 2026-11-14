import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def midpoint(m):
 r=m.sample_descriptors(np.array([[[1.,0.],[0.,1.]]]),np.array([[.5,0.]]),np.ones(2),np.zeros(2));assert_allclose(r['descriptors'],[[2**-.5,2**-.5]]);assert_array_equal(r['valid'],[True])
def outside(m):
 r=m.sample_descriptors(np.array([[[1.,0.],[0.,1.]]]),np.array([[-1.,0.]]),np.ones(2),np.zeros(2));assert_array_equal(r['descriptors'],[[0,0]]);assert_array_equal(r['valid'],[False])
def oracle(m):
 rng=np.random.default_rng(833);image=rng.normal(size=(32,64,32))[:,:,::2];points=rng.uniform(-5,70,(2048,4))[:,::2];stride=np.array([1.2,2.]);offset=np.array([.5,1.]);before=image.copy();r=m.sample_descriptors(image,points,stride,offset);expected=np.zeros((2048,16));valid=np.zeros(2048,bool)
 for k,p in enumerate(points):
  x,y=(p-offset)/stride
  if not (0<=x<=63 and 0<=y<=31):continue
  valid[k]=True;ix=int(x);iy=int(y);a=x-ix;b=y-iy;z=sum(image[min(iy+dy,31),min(ix+dx,63)]*(a if dx else 1-a)*(b if dy else 1-b) for dx in (0,1) for dy in (0,1));norm=sum(float(v)**2 for v in z)**.5
  if norm>1e-12:expected[k]=z/norm
 assert_allclose(r['descriptors'],expected,atol=1e-12);assert_array_equal(r['valid'],valid);assert_array_equal(image,before);assert not np.shares_memory(r['descriptors'],image)
def boundaries(m):
 image=np.array([[[3.,0.],[0.,1.]]]);r=m.sample_descriptors(image,np.array([[.5,0.],[1.,0.]]),np.ones(2),np.zeros(2));assert_allclose(r['descriptors'],[[3/np.sqrt(10),1/np.sqrt(10)],[0,1]])
 r=m.sample_descriptors(np.full((1,1,1),1e-12),np.zeros((1,2)),np.ones(2),np.zeros(2));assert r['valid'][0] and r['descriptors'][0,0]==0
 r=m.sample_descriptors(np.ones((1,1,1)),np.empty((0,2)),np.ones(2),np.zeros(2));assert r['descriptors'].shape==(0,1)
def invalid(m):
 for image,s in [(np.ones((1,1,1),np.float32),np.ones(2)),(np.ones((1,1,1))*101,np.ones(2)),(np.ones((1,1,1)),np.zeros(2)),(np.ones((0,1,1)),np.ones(2))]:bad(lambda:m.sample_descriptors(image,np.zeros((1,2)),s,np.zeros(2)))
TESTS=[('Interpolated unit descriptor','public',midpoint),('Unsupported keypoint','public',outside),('Scalar bilinear oracle and noncontiguous scale','hidden',oracle),('Normalize after interpolation singleton and zero norm','hidden',boundaries),('Malformed descriptor grids','hidden',invalid)]
