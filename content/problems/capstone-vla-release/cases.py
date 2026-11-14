import numpy as np,hashlib
from numpy.testing import assert_allclose,assert_array_equal
def args():return [np.ones((1,2,1)),np.full((1,2,1),.5),np.ones((1,2),bool),np.array([[True,False]]),np.array([0],np.int64),np.array([0],np.int64),np.array([[-1.]]),np.array([[1.]]),np.zeros((1,1)),np.ones((1,1)),np.zeros((1,1)),.5,np.array([[100.,5.]]),.01,10.]
def first(m):
 r=m.vla_release(*args());assert_allclose(r['adapter'],[[.5]]);assert_array_equal(r['tokens'],[[[12],[12]]]);assert_allclose(r['actions'],[[[.5625],[.5625]]]);assert_allclose(r['embodiment_mse'],[.00390625]);assert np.isnan(r['task_mse'][1:]).all();assert r['decision']=='promote' and r['p95_ms']==5 and r['invalid_rate']==0;assert r['adapter_sha256']==hashlib.sha256(np.array([[.5]],dtype='<f8').tobytes()).hexdigest()
def second(m):
 a=args();a[12][0,1]=20;r=m.vla_release(*a);assert r['decision']=='hold' and r['p95_ms']==20
def oracle(m):
 a=args();a[0]=np.array([[[1.,2.],[2.,1.]],[[0.,1.],[1.,0.]]]);a[1]=np.array([[[.3,.2],[.1,.4]],[[1.5,1.],[.8,1.2]]]);a[2]=np.ones((2,2),bool);a[3]=np.array([[True,False],[True,False]]);a[4]=np.array([0,1],np.int64);a[5]=np.array([1,2],np.int64);a[6]=np.array([[-1.,-1.],[0.,0.]]);a[7]=np.array([[1.,1.],[2.,2.]]);a[8]=np.array([[.1,.2],[.3,-.1]]);a[9]=np.array([[.4],[-.2]]);a[10]=np.array([[.1,.3]]);a[12]=np.ones((2,2));a[11]=.2
 expected=a[10].copy()
 for channel in range(2):
  grad=0
  for batch in range(2):
   x=a[0][batch,0];f=sum(x[j]*a[9][j,0] for j in range(2));pred=sum(x[j]*a[8][j,channel] for j in range(2))+f*a[10][0,channel];target=a[1][batch,0,channel]-a[6][batch,channel]-1;grad+=f*(pred-target)
  expected[0,channel]-=.2*grad/2
 r=m.vla_release(*a);assert_allclose(r['adapter'],expected)
 for batch in range(2):
  errs=[]
  for channel in range(2):
   x=a[0][batch,1];raw=x@a[8][:,channel]+(x@a[9][:,0])*expected[0,channel];token=min(15,int(np.floor(8*(np.clip(raw,-1,1)+1))));value=a[6][batch,channel]+(token+.5)/8;assert r['tokens'][batch,1,channel]==token;errs.append((value-a[1][batch,1,channel])**2)
  assert_allclose(r['embodiment_mse'][batch],np.mean(errs))
def masks(m):
 a=args();a[0][0,1]=10;a[8][:]=1;a[11]=0;r=m.vla_release(*a);assert r['invalid_rate']==1 and r['decision']=='hold'
 a=args();a[1][0,1]=-.5;r=m.vla_release(*a);assert_allclose(r['adapter'],[[.5]]);assert r['decision']=='hold'
def invalid(m):
 for index,value in [(3,np.ones((1,2),bool)),(4,np.array([1],np.int64)),(7,np.array([[-1.]])),(11,True),(12,np.array([[-1.,2.]]))]:
  a=args();a[index]=value
  with np.testing.assert_raises(ValueError):m.vla_release(*a)
def scale(m):
 a=args();a[0]=np.ones((32,32,32))[:,:,::2]*.01;a[1]=np.zeros((32,32,16));a[2]=np.ones((32,32),bool);a[2][0,31]=False;a[3]=np.zeros((32,32),bool);a[3][:,0]=True;a[4]=np.zeros(32,np.int64);a[5]=np.zeros(32,np.int64);a[6]=-np.ones((1,16));a[7]=np.ones((1,16));a[8]=np.zeros((16,16));a[9]=np.eye(16)[:,::2];a[10]=np.zeros((8,16));a[12]=np.ones((32,32));r=m.vla_release(*a);assert_array_equal(r['tokens'][0,31],-np.ones(16,dtype=np.int64));assert_array_equal(r['actions'][0,31],np.zeros(16));assert not np.shares_memory(r['adapter'],a[10]);assert not a[10].any();assert r['decision']=='promote'
TESTS=[('Adapter and held-out action codec','public',first),('Serving latency holds release','public',second),('Independent scalar gradient and slices','hidden',oracle),('Training isolation and saturation','hidden',masks),('Invalid contracts','hidden',invalid),('Bounded noncontiguous scale','hidden',scale)]

def huge_scalar(m):
 a=args();a[11]=10**1000
 with np.testing.assert_raises(ValueError):m.vla_release(*a)
TESTS.append(("Huge Python integer rejected", "hidden", huge_scalar))
