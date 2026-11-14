import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def args():return [np.ones((1,1,1),bool),np.ones((1,1)),np.ones(1),np.array([5.]),np.eye(3),np.eye(4),np.zeros((4,4)),.5,10.,0.,False]
def first(m):
 a=args();r=m.grounded_perception(*a);assert_allclose(r['centroids'],[[0,0,1]]);assert_array_equal(r['valid'],[True]);b=np.zeros((4,4));b[2,2]=.5;assert_allclose(r['bev'],b);assert r['decision']=='promote' and r['p95_ms']==5 and r['invalid_fraction']==0
def second(m):
 a=args();a[1][:]=0;a[-1]=True;r=m.grounded_perception(*a);assert np.isnan(r['centroids']).all();assert not r['valid'].any();assert r['decision']=='rollback' and r['invalid_fraction']==1
def oracle(m):
 rng=np.random.default_rng(44);a=args();a[0]=rng.random((8,3,4))>.4;a[1]=rng.uniform(.1,1,(3,4));a[2]=rng.random(8);a[3]=np.arange(8,dtype=float);a[4]=np.array([[2.,0,.5],[0,3.,.7],[0,0,1.]]);a[5][:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]];a[5][:3,3]=[.2,-.3,.1];a[6][:]=2;a[9]=1
 r=m.grounded_perception(*a);count=np.zeros((4,4));expected=np.full((8,3),np.nan);eligible=0;valid=0
 for i in range(8):
  if a[2][i]<.5:continue
  eligible+=1;points=[]
  for y in range(3):
   for x in range(4):
    if a[0][i,y,x]:
     z=a[1][y,x];points.append([-(y-.7)*z/3+.2,(x-.5)*z/2-.3,z+.1])
  if points:
   p=np.mean(points,axis=0);c=int(np.floor(p[0]+2));row=int(np.floor(p[1]+2))
   if 0<=c<4 and 0<=row<4:expected[i]=p;count[row,c]+=1;valid+=1
 assert_allclose(r['centroids'],expected,equal_nan=True);assert_allclose(r['bev'],1+.5*count);assert_allclose(r['invalid_fraction'],1-valid/eligible)
def failures(m):
 a=args();a[2][:]=0;r=m.grounded_perception(*a);assert r['decision']=='hold' and r['invalid_fraction']==1
 a=args();a[5][0,3]=2;assert not m.grounded_perception(*a)['valid'].any()
 a=args();a[3][:]=11;assert m.grounded_perception(*a)['decision']=='hold'
def denominator(m):
 a=args();a[0]=np.eye(3,dtype=bool).reshape(3,1,3);a[1]=np.ones((1,3));a[2]=np.array([1.,0.,1.]);a[3]=np.ones(3);a[9]=.5;r=m.grounded_perception(*a);assert_array_equal(r['valid'],[True,False,False]);assert r['invalid_fraction']==.5 and r['decision']=='promote'
def boundary(m):
 a=args();a[0]=np.eye(3,dtype=bool).reshape(3,1,3);a[1]=np.ones((1,3));a[2]=np.ones(3);a[3]=np.ones(3);a[9]=1/3;r=m.grounded_perception(*a);assert r['invalid_fraction']==1/3 and r['decision']=='promote'
def invalid(m):
 for index,value in [(4,np.zeros((3,3))),(5,np.diag([1.,1.,-1.,1.])),(1,np.array([[-1.]])),(10,1),(7,float('nan'))]:
  a=args();a[index]=value
  with np.testing.assert_raises(ValueError):m.grounded_perception(*a)
def scale(m):
 a=args();a[0]=np.ones((64,64,128),bool)[:,:,::2];a[1]=np.ones((64,128))[:,::2];a[2]=np.ones(64);a[3]=np.ones(64);a[4]=np.diag([100.,100.,1.]);saved=a[1].copy();r=m.grounded_perception(*a);assert r['valid'].all();assert r['bev'].sum()==32;assert_array_equal(a[1],saved)
 for v in r.values():
  if isinstance(v,np.ndarray):
   for inp in a:
    if isinstance(inp,np.ndarray):assert not np.shares_memory(v,inp)
TESTS=[('One grounded object','public',first),('Missing depth rollback','public',second),('Scalar frame oracle','hidden',oracle),('Threshold and boundary failures','hidden',failures),('Eligible query denominator','hidden',denominator),('Inclusive one-third gate boundary','hidden',boundary),('Malformed contracts','hidden',invalid),('Noncontiguous scale','hidden',scale)]

def huge_scalar(m):
 a=args();a[7]=10**1000
 with np.testing.assert_raises(ValueError):m.grounded_perception(*a)
TESTS.append(("Huge Python integer rejected", "hidden", huge_scalar))
