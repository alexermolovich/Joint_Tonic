import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def args(p,uv):return [p,np.zeros((len(p),32),np.uint8),uv,np.zeros((len(uv),32),np.uint8),np.eye(4),np.array([1.,1.,0.,0.]),1.,256]
def collision(m):
 a=args(np.tile([0.,0.,1.],(2,1)),np.zeros((1,2)));a[6]=0;a[7]=0;r=m.associate_map_features(*a);assert_array_equal(r['feature_indices'],[0,-1]);assert_array_equal(r['hamming'],[0,-1]);assert_allclose(r['squared_error'],[0,np.inf])
def bits(m):
 a=args(np.array([[0.,0.,1.]]),np.zeros((1,2)));a[1][0,0]=255;a[7]=7;assert m.associate_map_features(*a)['feature_indices'][0]==-1;a[7]=8;r=m.associate_map_features(*a);assert r['feature_indices'][0]==0 and r['hamming'][0]==8
def oracle(m):
 rng=np.random.default_rng(846);p=rng.uniform(-1,1,(128,6))[:,::2];p[:,2]+=3;uv=rng.uniform(-.5,.5,(160,4))[:,::2];a=args(p,uv);a[1]=rng.integers(0,256,(128,64),dtype=np.uint8)[:,::2];a[3]=rng.integers(0,256,(160,64),dtype=np.uint8)[:,::2];a[4][:3,:3]=np.array([[0.,-1,0],[1,0,0],[0,0,1.]]);a[4][:3,3]=[.1,.2,.3];a[6]=.3;a[7]=128;before=a[1].copy();r=m.associate_map_features(*a);proposals=[]
 for i,point in enumerate(p):
  camera=a[4][:3,:3]@point+a[4][:3,3];projected=camera[:2]/camera[2];options=[]
  for j,pixel in enumerate(uv):
   dist=sum(float(x)**2 for x in pixel-projected);ham=sum((int(x)^int(y)).bit_count() for x,y in zip(a[1][i],a[3][j]))
   if dist<=.09 and ham<=128:options.append((ham,dist,j))
  if options:ham,dist,j=min(options);proposals.append((ham,dist,i,j))
 indices=np.full(128,-1);hamming=np.full(128,-1);error=np.full(128,np.inf);used=set()
 for ham,dist,i,j in sorted(proposals):
  if j not in used:used.add(j);indices[i]=j;hamming[i]=ham;error[i]=dist
 assert_array_equal(r['feature_indices'],indices);assert_array_equal(r['hamming'],hamming);assert_allclose(r['squared_error'],error);assert_array_equal(a[1],before);assert not np.shares_memory(r['feature_indices'],a[1])
def edges(m):
 a=args(np.tile([0.,0.,1.],(2,1)),np.array([[0.,0.],[1.,0.]]));r=m.associate_map_features(*a);assert_array_equal(r['feature_indices'],[0,-1])
 a=args(np.array([[0.,0.,1e-6],[0.,0.,-1.]]),np.zeros((1,2)));assert (m.associate_map_features(*a)['feature_indices']==-1).all()
 a=args(np.empty((0,3)),np.empty((0,2)));assert m.associate_map_features(*a)['feature_indices'].shape==(0,)
 a=args(np.array([[0.,0.,1.]]),np.array([[1.,0.]]));assert m.associate_map_features(*a)['feature_indices'][0]==0
def invalid(m):
 a=args(np.zeros((1,3)),np.zeros((1,2)));a[1]=a[1].astype(np.int64);bad(lambda:m.associate_map_features(*a));a=args(np.zeros((1,3)),np.zeros((1,2)));a[6]=10**1000;bad(lambda:m.associate_map_features(*a));a[6]=1;a[7]=True;bad(lambda:m.associate_map_features(*a));a[7]=1;a[4][0,0]=2;bad(lambda:m.associate_map_features(*a))
TESTS=[('Deterministic feature collision','public',collision),('Packed byte bit count','public',bits),('Independent scalar projection bit-count proposal oracle at scale','hidden',oracle),('No retry depth cutoff radius equality and empty inputs','hidden',edges),('Invalid descriptor dtype camera or scalars','hidden',invalid)]
