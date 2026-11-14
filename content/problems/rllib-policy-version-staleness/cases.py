"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):
    np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)

def run(m,v,versions,counts,lag):return m.policy_staleness_report(v,np.array(versions,dtype=np.int64),np.array(counts,dtype=np.int64),lag)
def example1(m):
 r=run(m,10,[10,7,12],[2,6,4],2);same(r['lag'],[0,3,-2]);same(r['future'],[False,False,True]);same(r['stale'],[False,True,False]);same(r['accepted'],[True,False,False]);assert r['accepted_samples']==2 and r['rejected_samples']==10 and r['mean_known_lag']==2.25
 assert r['lag'].dtype==np.int64 and r['accepted'].dtype==np.bool_
def example2(m):
 r=run(m,0,[1],[5],0);same(r['lag'],[-1]);assert r['accepted_samples']==0 and r['rejected_samples']==5 and np.isnan(r['mean_known_lag'])
def edges(m):
 high=2**63-1;r=run(m,high,[0,high],[10**6,10**6],high);assert r['mean_known_lag']==high/2 and r['accepted_samples']==2*10**6;same(r['lag'],[high,0])
 r=run(m,high,[high-1],[1],1);assert r['lag'][0]==1 and r['accepted'][0]
 r=run(m,0,[],[],0);assert r['lag'].shape==(0,) and np.isnan(r['mean_known_lag'])
 r=run(m,3,[1,3],[0,0],2);same(r['accepted'],[True,True]);assert np.isnan(r['mean_known_lag'])
def oracle_scale(m):
 versions=np.arange(200000,dtype=np.int64)[::2];counts=(np.arange(200000,dtype=np.int64)%1001)[::2];before=[versions.copy(),counts.copy()];r=m.policy_staleness_report(123456,versions,counts,321)
 lags=[123456-int(v) for v in versions];keep=[0<=v<=321 for v in lags];known=[(l,int(n)) for l,n in zip(lags,counts) if l>=0];den=sum(n for l,n in known)
 same(r['lag'],lags);same(r['accepted'],keep);assert r['accepted_samples']==sum(int(n) for n,k in zip(counts,keep) if k);assert r['rejected_samples']==sum(int(n) for n,k in zip(counts,keep) if not k);assert r['mean_known_lag']==sum(l*n for l,n in known)/den
 for a,b in zip(before,[versions,counts]):np.testing.assert_array_equal(a,b)
def invalid(m):
 for args in [(True,[0],[1],0),(0,[-1],[1],0),(0,[0],[-1],0),(0,[0],[10**6+1],0),(0,[0],[],0),(0,[0],[1],-1)]:reject(lambda:run(m,*args))
 reject(lambda:m.policy_staleness_report(1,np.array([0.]),np.array([1],dtype=np.int64),0))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
