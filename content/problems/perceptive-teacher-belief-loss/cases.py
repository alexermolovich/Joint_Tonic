import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def args():return [np.array([[[1.]]]),np.zeros((1,1,1)),np.array([[[2.]]]),np.zeros((1,1,1)),np.ones((1,1),bool),np.ones((1,1,1),bool),np.array([2.]),np.array([1.]),np.array([2.,.5])]

def first(m):
    r=m.teacher_belief_loss(*args());assert_allclose(r['components'],[.25,4]);assert_array_equal(r['counts'],[1,1]);assert r['counts'].dtype==np.int64 and isinstance(r['loss'],float);assert r['loss']==2.5;assert_allclose(r['action_gradient'],1);assert_allclose(r['reconstruction_gradient'],2)

def absent(m):
    a=args();a[4][:]=False;a[5][:]=False;r=m.teacher_belief_loss(*a);assert_array_equal(r['counts'],[0,0]);assert_array_equal(r['components'],[0,0]);assert r['loss']==0;assert_array_equal(r['action_gradient'],0);assert_array_equal(r['reconstruction_gradient'],0)

def gradient(m):
    rng=np.random.default_rng(561);a=[rng.normal(size=(2,3,2)),rng.normal(size=(2,3,2)),rng.normal(size=(2,3,3)),rng.normal(size=(2,3,3)),np.array([[1,0,1],[0,1,0]],bool),rng.random((2,3,3))>.4,np.array([.5,2.]),np.array([.2,1.,3.]),np.array([.7,1.3])];r=m.teacher_belief_loss(*a)
    for slot,key in [(0,'action_gradient'),(2,'reconstruction_gradient')]:
        numerical=np.empty_like(a[slot])
        for index in np.ndindex(a[slot].shape):
            up=[x.copy() for x in a];down=[x.copy() for x in a];up[slot][index]+=1e-5;down[slot][index]-=1e-5;numerical[index]=(m.teacher_belief_loss(*up)['loss']-m.teacher_belief_loss(*down)['loss'])/2e-5
        assert_allclose(r[key],numerical,rtol=1e-6,atol=1e-8)
    na=int(a[4].sum())*2;nz=int(a[5].sum());la=sum(((a[0][b,t,d]-a[1][b,t,d])/a[6][d])**2 for b,t,d in np.ndindex(a[0].shape) if a[4][b,t])/na;lz=sum(((a[2][b,t,d]-a[3][b,t,d])/a[7][d])**2 for b,t,d in np.ndindex(a[2].shape) if a[5][b,t,d])/nz;assert_allclose(r['components'],[la,lz]);assert_array_equal(r['counts'],[na,nz])

def scale(m):
    rng=np.random.default_rng(562);a=rng.normal(size=(64,128,64))[:,:,::2];z=rng.normal(size=(64,128,128))[:,:,::2];inputs=[a,np.zeros_like(a),z,np.zeros_like(z),rng.random((64,128))>.2,rng.random(z.shape)>.3,np.ones(32)*2,np.ones(64)*3,np.array([1.,2.])];before=[x.copy() for x in inputs];r=m.teacher_belief_loss(*inputs);assert_array_equal(r['counts'],[32*inputs[4].sum(),inputs[5].sum()]);assert_allclose(r['components'],[np.mean((a[inputs[4]]/2)**2),np.mean((z[inputs[5]]/3)**2)])
    for x,y in zip(inputs,before):assert_array_equal(x,y)
    for out in [r['components'],r['counts'],r['action_gradient'],r['reconstruction_gradient']]:
        for x in inputs:assert not np.shares_memory(out,x)
    inputs=[np.empty((0,1,1)),np.empty((0,1,1)),np.empty((0,1,2)),np.empty((0,1,2)),np.empty((0,1),bool),np.empty((0,1,2),bool),[1],[1,1],[1,1]];r=m.teacher_belief_loss(*inputs);assert r['loss']==0 and r['action_gradient'].shape==(0,1,1)

def invalid(m):
    for slot,value in [(1,[[[np.nan]]]),(0,[[[11]]]),(6,[0]),(7,[101]),(8,[1,-1]),(4,[[1]]),(5,[[[0]]]),(0,[[[1+0j]]]),(0,[[[10**1000]]])]:
        a=args();a[4][:]=False;a[5][:]=False;a[slot]=value;bad(lambda:m.teacher_belief_loss(*a))
TESTS=[('Scaled teacher and reconstruction example','public',first),('Absent components remain zero','public',absent),('Independent component oracle and frozen-target finite differences','hidden',gradient),('Strided maximum scale empty batches and no aliases','hidden',scale),('Invalid values including masked labels','hidden',invalid)]
