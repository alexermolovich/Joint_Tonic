import numpy as np,json,hashlib,hmac
from numpy.testing import assert_array_equal,assert_allclose
def args():return [np.array([[4.,5.],[2.,3.]]),np.array([.9,.8]),np.array([.1,.1]),np.array([[8,4],[4,4]],np.int64),np.array([[0,1],[1,2]],np.int64),[b'a',b'b'],'rgb-0-1',b'k'*32,.8,10.,8,.2,False]
def first(m):
 a=args();r=m.edge_deployment(*a);assert_array_equal(r['buffer_ids'],[[0,0],[0,0]]);assert_array_equal(r['allocated_bytes'],[8,4]);assert_allclose(r['p95_ms'],[5,3]);assert r['candidate']==0 and r['decision']=='promote';record=json.loads(r['manifest']);assert record==dict(allocated_bytes=8,candidate=0,model_sha256=hashlib.sha256(b'a').hexdigest(),preprocessing='rgb-0-1',schema=1);payload=json.dumps(record,sort_keys=True,separators=(',',':')).encode();assert r['sha256']==hashlib.sha256(payload).hexdigest();assert r['signature']==hmac.new(b'k'*32,payload,hashlib.sha256).hexdigest()
def second(m):
 a=args();a[2][0]=.3;a[-1]=True;r=m.edge_deployment(*a);assert r['candidate']==0 and r['decision']=='rollback';assert r['manifest']==m.edge_deployment(*args())['manifest']
def lifetimes(m):
 a=args();a[3]=np.array([[8,4,3,7],[4,4,3,3]],np.int64);a[4]=np.array([[0,2],[0,1],[1,3],[2,4]],np.int64);a[10]=20;r=m.edge_deployment(*a);assert_array_equal(r['buffer_ids'],[[0,1,1,0],[0,1,1,0]]);assert_array_equal(r['allocated_bytes'],[12,8])
def selection(m):
 a=args();a[1][:]=.8;r=m.edge_deployment(*a);assert r['candidate']==1
 a[0][:]=3;r=m.edge_deployment(*a);assert r['candidate']==0
 a[10]=1;r=m.edge_deployment(*a);assert r['candidate']==-1 and r['manifest'] is None and r['signature'] is None and r['decision']=='hold'
def identity(m):
 a=args();r=m.edge_deployment(*a);a[6]='bgr-mean';q=m.edge_deployment(*a);assert r['signature']!=q['signature'];a=args();a[5][0]=b'changed';assert r['sha256']!=m.edge_deployment(*a)['sha256']
def invalid(m):
 for idx,v in [(0,np.zeros((2,2))),(4,np.array([[0,0],[1,2]],np.int64)),(7,b'x'),(10,True),(6,'BGR'),(5,[b'a',bytearray(b'b')])]:
  a=args();a[idx]=v
  with np.testing.assert_raises(ValueError):m.edge_deployment(*a)
def scale(m):
 a=args();a[0]=np.ones((16,256))[:,::2];a[1]=np.ones(16);a[2]=np.zeros(16);a[3]=np.ones((16,128),np.int64)[:,::2]*16;a[4]=np.array([[i,i+1] for i in range(64)],np.int64);a[5]=[bytes([i])*4096 for i in range(16)];a[10]=16;r=m.edge_deployment(*a);assert_array_equal(r['buffer_ids'],np.zeros((16,64),np.int64));assert_array_equal(r['allocated_bytes'],np.full(16,16));assert r['candidate']==0;assert not np.shares_memory(r['buffer_ids'],a[3]);assert (a[3]==16).all()
TESTS=[('Buffer reuse and signed package','public',first),('Drift retains rejected candidate evidence','public',second),('Half-open simultaneous lifetimes','hidden',lifetimes),('Selection ties and no candidate','hidden',selection),('Preprocessing and artifact binding','hidden',identity),('Malformed contracts','hidden',invalid),('Noncontiguous scale','hidden',scale)]

def huge_scalar(m):
 a=args();a[8]=10**1000
 with np.testing.assert_raises(ValueError):m.edge_deployment(*a)
TESTS.append(("Huge Python integer rejected", "hidden", huge_scalar))
