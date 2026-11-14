import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def ramp(m):
 image=np.tile(np.linspace(0,1,5),(5,1));r=m.select_gradient_points(image,5,.1);assert_array_equal(r['coordinates'],[[1,1]]);assert_allclose(r['scores'],[.25])
def constant(m):
 r=m.select_gradient_points(np.ones((3,3)),1,0);assert r['coordinates'].shape==(0,2) and r['coordinates'].dtype==np.int64;assert r['scores'].shape==(0,)
def oracle(m):
 rng=np.random.default_rng(820);image=rng.random((128,512))[:,::2];before=image.copy();r=m.select_gradient_points(image,17,.2);coords=[];scores=[];h,w=image.shape
 for sy in range(0,h,17):
  for sx in range(0,w,17):
   options=[]
   for y in range(max(sy,1),min(sy+17,h-1)):
    for x in range(max(sx,1),min(sx+17,w-1)):
     dx=(float(image[y,x+1])-float(image[y,x-1]))/2;dy=(float(image[y+1,x])-float(image[y-1,x]))/2;s=(dx*dx+dy*dy)**.5
     if s>.2:options.append((-s,y*w+x,x,y))
   if options:
    s,_,x,y=min(options);coords.append([x,y]);scores.append(-s)
 assert_array_equal(r['coordinates'],coords);assert_allclose(r['scores'],scores);assert_array_equal(image,before);assert not np.shares_memory(r['scores'],image)
def edges(m):
 image=np.tile(np.linspace(0,1,5),(5,1));r=m.select_gradient_points(image,2,.25);assert not len(r['scores'])
 r=m.select_gradient_points(image,2,.2);assert_array_equal(r['coordinates'],[[1,1],[2,1],[1,2],[2,2]])
 # One-pixel tiles retain every interior pixel in row-major order.
 r=m.select_gradient_points(image,1,.2);assert len(r['scores'])==9;assert_array_equal(r['coordinates'][0],[1,1]);assert_array_equal(r['coordinates'][-1],[3,3])
def invalid(m):
 for image,t,s in [(np.ones((2,3)),1,0),(np.ones((3,3)),True,0),(np.ones((3,3))*2,1,0),(np.ones((3,3)),1,-1),(np.ones((3,3),dtype=np.float32),1,0),(np.ones((3,3)),1,10**1000)]:bad(lambda:m.select_gradient_points(image,t,s))
TESTS=[('Spatial gradient tie','public',ramp),('No texture','public',constant),('Independent tiled scalar oracle at scale','hidden',oracle),('Border, partial tiles and strict threshold','hidden',edges),('Invalid image contract','hidden',invalid)]
