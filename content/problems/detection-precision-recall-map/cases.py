import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def call(m,p,s,pl,pi,t,tl,ti,c=1,threshold=.5):return m.detection_map(np.asarray(p,dtype=float).reshape(-1,4),np.asarray(s,dtype=float),np.asarray(pl,dtype=np.int64),np.asarray(pi,dtype=np.int64),np.asarray(t,dtype=float).reshape(-1,4),np.asarray(tl,dtype=np.int64),np.asarray(ti,dtype=np.int64),c,threshold)
def example(m):
    a=[0,0,.2,.2];b=[.8,.8,1,1];r=call(m,[a,a,b],[.9,.8,.7],[0]*3,[0]*3,[a,b],[0,0],[0,0]);assert_allclose(r['precision'][0],[1,.5,2/3]);assert_allclose(r['recall'][0],[.5,.5,1]);assert_allclose(r['ap'],[5/6]);assert_allclose(r['mean_ap'],5/6)
def no_predictions(m):
    r=call(m,[],[],[],[],[[0,0,1,1]],[0],[0],2);assert r['ap'][0]==0 and np.isnan(r['ap'][1]) and r['mean_ap']==0
def identity(m):
    a=[0,0,1,1];r=call(m,[a,a],[.8,.8],[0,0],[9,0],[a],[0],[0]);assert_allclose(r['precision'][0],[0,.5]);assert_allclose(r['ap'],[.5])
    r=call(m,[a],[1],[1],[0],[a],[0],[0],2);assert r['ap'][0]==0 and np.isnan(r['ap'][1]);assert_allclose(r['recall'][1],[0])
def no_fallback(m):
    a=[0,0,1,1];b=[0,0,.9,1];r=call(m,[a,a],[.9,.8],[0,0],[0,0],[a,b],[0,0],[0,0]);assert_allclose(r['recall'][0],[.5,.5]);assert_allclose(r['ap'],[.5])
    r=call(m,[[0,0,.5,1]],[1],[0],[0],[a],[0],[0],threshold=.5);assert_allclose(r['ap'],[1])
def empty(m):
    r=call(m,[],[],[],[],[],[],[],2);assert np.isnan(r['ap']).all() and r['mean_ap']==0;assert all(a.shape==(0,) for a in r['precision'])
def invalid(m):
    for p,s,pl in [([[0,0,0,1]],[1],[0]),([[0,0,1,1]],[1.1],[0]),([[0,0,1,1]],[1],[1])]:
        with np.testing.assert_raises(ValueError):call(m,p,s,pl,[0],[],[],[])
TESTS=[('Interpolated AP and duplicate','public',example),('Unobserved class vs zero recall','public',no_predictions),('Image class and tie identities','hidden',identity),('No duplicate fallback and IoU equality','hidden',no_fallback),('Empty evaluation','hidden',empty),('Validation','hidden',invalid)]

def scale_storage(m):
    n=512;b=np.tile([0.,0.,1.,1.,0.,0.,1.,1.],(n,1))[:,:4];labels=np.arange(n,dtype=np.int64)%4;images=np.arange(n,dtype=np.int64);scores=np.linspace(0,1,n);saved=b.copy();r=m.detection_map(b,scores,labels,images,b.copy(),labels.copy(),images.copy(),4,1.)
    assert_allclose(r['ap'],1);assert r['mean_ap']==1;assert_allclose(b,saved)
    for out in [r['ap']]+r['precision']+r['recall']:assert not np.shares_memory(out,b)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
