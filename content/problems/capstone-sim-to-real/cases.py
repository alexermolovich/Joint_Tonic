import numpy as np,hashlib,json,math
from numpy.testing import assert_allclose,assert_array_equal
def args():return [np.ones((8,4),bool),np.ones((8,4),bool),np.full((8,4),5.),7,.5,.2,10.]
def first(m):
 r=m.sim_to_real(*args());assert_array_equal(r['strata'],[0,1,2,3,0,1,2,3]);assert_array_equal(r['counts'],np.full((4,4),2));assert_allclose(r['rates'],1);assert_allclose(r['wilson'],np.tile([8/(8+1.959963984540054**2),1],(4,1)));assert r['decision']=='promote';assert_allclose(r['factors'][0],[.650038186641867,.9486069004847877]);record=dict(schema=1,seed=7,samples=8,friction=[.4,1.2],lighting=[.5,1.5],strata=4);assert r['distribution_sha256']==hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def second(m):
 a=args();a[0][[0,4],3]=False;r=m.sim_to_real(*a);assert r['mean_rate'][3]==.75 and r['worst_rate'][3]==0 and r['sim_real_gap'][0]==1 and r['decision']=='hold'
def missing(m):
 a=args();a[1][:,2]=False;r=m.sim_to_real(*a);assert np.isnan(r['rates'][:,2]).all() and np.isnan(r['wilson'][2]).all() and np.isnan(r['p95_ms'][2]);assert r['decision']=='hold'
 a=args();a[1][0,3]=False;a[0][0,3]=False;r=m.sim_to_real(*a);assert r['mean_rate'][3]==1 and r['decision']=='hold'
def oracle(m):
 rng=np.random.default_rng(5);a=args();a[0]=rng.random((23,4))>.3;a[1]=rng.random((23,4))>.2;a[2]=rng.uniform(1,20,(23,4));r=m.sim_to_real(*a)
 for b in range(4):
  for d in range(4):
   vals=[int(a[0][i,d]) for i in range(23) if i%4==b and a[1][i,d]];assert r['counts'][b,d]==len(vals)
   if vals:assert_allclose(r['rates'][b,d],sum(vals)/len(vals))
 for d in range(4):
  vals=[float(a[2][i,d]) for i in range(23) if a[1][i,d]];assert r['p95_ms'][d]==sorted(vals)[math.ceil(.95*len(vals))-1]
 u=np.random.default_rng(7).random((23,2))
 for i in range(23):assert_allclose(r['factors'][i],[.4+.4*((i%4)//2+u[i,0]),.5+.5*(i%2+u[i,1])])
def invalid(m):
 for idx,v in [(0,np.ones((3,4),bool)),(1,np.ones((8,4),np.int64)),(3,True),(4,float('nan')),(2,np.full((8,4),-1.))]:
  a=args();a[idx]=v
  with np.testing.assert_raises(ValueError):m.sim_to_real(*a)
def scale(m):
 a=args();a[0]=np.ones((1024,8),bool)[:,::2];a[1]=a[0].copy();a[2]=np.ones((1024,8))[:,::2];r=m.sim_to_real(*a);assert_array_equal(r['counts'],np.full((4,4),256));assert r['decision']=='promote';assert_allclose(r['factors'],m.sim_to_real(*a)['factors']);a[3]=8;q=m.sim_to_real(*a);assert not np.array_equal(r['factors'],q['factors']);assert not np.shares_memory(r['counts'],a[0]);assert a[0].all()
TESTS=[('Complete four-domain evidence','public',first),('Worst bucket blocks transfer','public',second),('Missing is not failure or success','hidden',missing),('Independent count and factor oracle','hidden',oracle),('Malformed contracts','hidden',invalid),('Reproducible noncontiguous scale','hidden',scale)]

def huge_scalar(m):
 a=args();a[4]=10**1000
 with np.testing.assert_raises(ValueError):m.sim_to_real(*a)
TESTS.append(("Huge Python integer rejected", "hidden", huge_scalar))
