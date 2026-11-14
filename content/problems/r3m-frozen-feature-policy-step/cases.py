import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def args():return [np.array([[1.],[2.]]),np.empty((2,0)),np.array([[1.],[0.]]),np.array([True,False]),np.array([False,True]),np.zeros((1,1)),np.zeros(1),.1]

def one(m):
    r=m.frozen_policy_step(*args());assert_allclose(r['weight'],[[.2]]);assert_allclose(r['bias'],[.2]);assert_allclose(r['predictions'],[[.4],[.6]]);assert r['train_loss_before']==1;assert_allclose(r['train_loss_after'],.36);assert_allclose(r['evaluation_loss'],.36)

def zero(m):
    a=args();a[-1]=0;a[4][:]=False;r=m.frozen_policy_step(*a);assert_array_equal(r['weight'],[[0]]);assert_array_equal(r['predictions'],[[0],[0]]);assert r['train_loss_after']==1 and np.isnan(r['evaluation_loss'])

def oracle(m):
    rng=np.random.default_rng(557);z=rng.normal(size=(32,8));s=rng.normal(size=(32,3));a=rng.uniform(-1,1,(32,2));t=np.arange(32)%3==0;e=~t;w=rng.normal(size=(11,2));b=rng.normal(size=2);x=np.c_[z,s];res=x[t]@w+b-a[t];gw=np.zeros_like(w);gb=np.zeros_like(b)
    for i in np.flatnonzero(t):
        for k in range(2):
            error=sum(x[i,j]*w[j,k] for j in range(11))+b[k]-a[i,k];gb[k]+=2*error/(t.sum()*2)
            for j in range(11):gw[j,k]+=2*x[i,j]*error/(t.sum()*2)
    out=m.frozen_policy_step(z,s,a,t,e,w,b,.001);assert_allclose(out['weight'],w-.001*gw);assert_allclose(out['bias'],b-.001*gb);assert_allclose(out['train_loss_before'],np.mean(res**2));assert_allclose(out['evaluation_loss'],np.mean((out['predictions'][e]-a[e])**2))
    changed=a.copy();changed[e]*=-1;second=m.frozen_policy_step(z,s,changed,t,e,w,b,.001);assert_array_equal(out['weight'],second['weight']);assert_array_equal(out['bias'],second['bias'])
    z=np.ones((4096,128))[:,::2];s=np.ones((4096,32));a=np.zeros((4096,16));t=np.arange(4096)%2==0;e=~t;w=np.ones((96,16))*.01;b=np.zeros(16);before=z.copy();out=m.frozen_policy_step(z,s,a,t,e,w,b,.001);assert out['predictions'].shape==(4096,16);assert_array_equal(z,before);assert not np.shares_memory(out['weight'],w);assert_allclose(out['weight'],.01-.001*2*.96/16)

def invalid(m):
    for key,value in [(7,10**1000),(3,np.array([False,False])),(4,np.array([True,True])),(2,np.array([[0.],[np.nan]])),(0,np.array([[1.],[11.]]))]:
        a=args();a[key]=value;bad(lambda:m.frozen_policy_step(*a))
TESTS=[('Frozen features one policy update','public',one),('Zero learning rate without evaluation evidence','public',zero),('Scalar gradient oracle held-out invariance noncontiguous scale','hidden',oracle),('Invalid split scalar or policy inputs','hidden',invalid)]
